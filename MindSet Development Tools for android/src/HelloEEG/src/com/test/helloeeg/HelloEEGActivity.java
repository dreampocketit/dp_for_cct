package com.test.helloeeg;

import android.app.Activity;
import android.bluetooth.BluetoothAdapter;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import java.util.*;
import android.util.Log;
import android.view.View;
import android.webkit.WebSettings;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import com.neurosky.thinkgear.*;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;
import org.json.JSONObject;

public class HelloEEGActivity extends Activity {
	BluetoothAdapter bluetoothAdapter;
    WebView browser;
	
	TextView tv;
	Button b;

    List delta_win = new LinkedList();
	
	TGDevice tgDevice;
	final boolean rawEnabled = false;
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        tv = (TextView)findViewById(R.id.textView1);
        tv.setText("");
        tv.append("Android version: " + Integer.valueOf(android.os.Build.VERSION.SDK) + "\n" );
        bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        if(bluetoothAdapter == null) {
        	// Alert user that Bluetooth is not available
        	Toast.makeText(this, "Bluetooth not available", Toast.LENGTH_LONG).show();
        	finish();
        	return;
        }else {
        	/* create the TGDevice */
        	tgDevice = new TGDevice(bluetoothAdapter, handler);
        }


        browser = (WebView) findViewById(R.id.webView);

        //for open in this webview
        WebView myWebView = (WebView) findViewById(R.id.webView);
        myWebView.setWebViewClient(new WebViewClient());

        //for enable js
        WebSettings webSettings = browser.getSettings();
        webSettings.setJavaScriptEnabled(true);


        browser.loadUrl("http://54.186.186.248/cct_experiment/");

    }
    
    @Override
    public void onDestroy() {
    	tgDevice.close();
        super.onDestroy();
    }
    /**
     * Handles messages from TGDevice
     */
    private final Handler handler = new Handler() {
        @Override
        public void handleMessage(Message msg) {
        switch (msg.what) {
            case TGDevice.MSG_STATE_CHANGE:
                switch (msg.arg1) {
	                case TGDevice.STATE_IDLE:
	                    break;
	                case TGDevice.STATE_CONNECTING:
	                	tv.append("Connecting...\n");
	                	break;
	                case TGDevice.STATE_CONNECTED:
	                	tv.append("Connected.\n");
	                	tgDevice.start();
	                    break;
	                case TGDevice.STATE_NOT_FOUND:
	                	tv.append("Can't find\n");
	                	break;
	                case TGDevice.STATE_NOT_PAIRED:
	                	tv.append("not paired\n");
	                	break;
	                case TGDevice.STATE_DISCONNECTED:
	                	tv.append("Disconnected mang\n");
                }

                break;
            case TGDevice.MSG_POOR_SIGNAL:
            		//signal = msg.arg1;
            		tv.append("PoorSignal: " + msg.arg1 + "\n");
                break;
            case TGDevice.MSG_RAW_DATA:
            		//raw1 = msg.arg1;
            		//tv.append("Got raw: " + msg.arg1 + "\n");
            	break;
            case TGDevice.MSG_ATTENTION:
            		//att = msg.arg1;
            		tv.append("Attention: " + msg.arg1 + "\n");
            		//Log.v("HelloA", "Attention: " + att + "\n");
            	break;
            case TGDevice.MSG_MEDITATION:

            	break;
            case TGDevice.MSG_BLINK:
            		//tv.append("Blink: " + msg.arg1 + "\n");
            	break;
            case TGDevice.MSG_LOW_BATTERY:
            	Toast.makeText(getApplicationContext(), "Low battery!", Toast.LENGTH_SHORT).show();
            	break;
            case TGDevice.MSG_EEG_POWER:
                TGEegPower ep = (TGEegPower)msg.obj;

                // a window for time shift
                if(delta_win.size()>10){
                    delta_win.remove(0);
                    delta_win.add(ep.delta);
                    tv.append("Delta: " + delta_win);
                }else{
                    delta_win.add(ep.delta);
                }

            default:
            	break;
        }
        }
    };

    public void printPower(View view) {
        sendData(delta_win);
    }
    
    public void doStuff(View view) {
    	if(tgDevice.getState() != TGDevice.STATE_CONNECTING && tgDevice.getState() != TGDevice.STATE_CONNECTED)
    		tgDevice.connect(rawEnabled);   
    	//tgDevice.ena
    }

    public void sendData(List data){

        HttpClient httpClient = new DefaultHttpClient();

        try {
            HttpPost request = new HttpPost("http://54.186.186.248/cct_experiment/get_data");

            StringEntity se = new StringEntity("details={\"delta\":"+data.toString()+"}");


            request.addHeader("content-type", "application/x-www-form-urlencoded");
            request.setEntity(se);
            HttpResponse response = httpClient.execute(request);
            String responseStr = EntityUtils.toString(request.getEntity());
            tv.setText(responseStr);

            // handle response here...
        }catch (Exception ex) {
            // handle exception here
        } finally {
            httpClient.getConnectionManager().shutdown();
        }


    }
}