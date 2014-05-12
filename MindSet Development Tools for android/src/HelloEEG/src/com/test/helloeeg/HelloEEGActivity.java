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

    String main_url = "http://140.114.135.43";

    List delta_win = new LinkedList();
    List theta_win = new LinkedList();
    List lowAlpha_win = new LinkedList();
    List highAlpha_win = new LinkedList();
    List lowBeta_win = new LinkedList();
    List highBeta_win = new LinkedList();
    List lowGamma_win = new LinkedList();
    List midGamma_win = new LinkedList();
	
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


        browser.loadUrl(main_url+"/for_android/");

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
                if(delta_win.size()>7){


                    delta_win.remove(0);
                    theta_win.remove(0);
                    lowAlpha_win.remove(0);
                    highAlpha_win.remove(0);
                    lowBeta_win.remove(0);
                    highBeta_win.remove(0);
                    lowGamma_win.remove(0);
                    midGamma_win.remove(0);

                    String s = "Delta: "+delta_win+"\n"+
                            "theta: "+theta_win+"\n"+
                            "lowAlpha: "+lowAlpha_win+"\n"+
                            "highAlpha: "+highAlpha_win+"\n"+
                            "lowBeta: "+lowBeta_win+"\n"+
                            "highBeta: "+highBeta_win+"\n"+
                            "lowGamma: "+lowGamma_win+"\n"+
                            "midGamma: "+midGamma_win+"\n";
                    tv.setText(s);
                }


                delta_win.add(ep.delta);
                theta_win.add(ep.theta);
                lowAlpha_win.add(ep.lowAlpha);
                highAlpha_win.add(ep.highAlpha);
                lowBeta_win.add(ep.lowBeta);
                highBeta_win.add(ep.highBeta);
                lowGamma_win.add(ep.lowGamma);
                midGamma_win.add(ep.midGamma);

            default:
            	break;
        }
        }
    };

    public void diffBtn(View view) {

        final String s = "["+delta_win.toString()+","+
                    theta_win.toString()+","+
                    lowAlpha_win.toString()+","+
                    highAlpha_win.toString()+","+
                    lowBeta_win.toString()+","+
                    highBeta_win.toString()+","+
                    lowGamma_win.toString()+","+
                    midGamma_win.toString()+"]";
        new Thread(new Runnable() {
            public void run() {
                sendData(s,main_url+"/for_android/get_diff_data");
            }
        }).start();

    }

    public void easyBtn(View view) {
        final String s = "["+delta_win.toString()+","+
                theta_win.toString()+","+
                lowAlpha_win.toString()+","+
                highAlpha_win.toString()+","+
                lowBeta_win.toString()+","+
                highBeta_win.toString()+","+
                lowGamma_win.toString()+","+
                midGamma_win.toString()+"]";
        new Thread(new Runnable() {
            public void run() {
                sendData(s,main_url+"/for_android/get_easy_data");
            }
        }).start();

    }
    
    public void doStuff(View view) {
    	if(tgDevice.getState() != TGDevice.STATE_CONNECTING && tgDevice.getState() != TGDevice.STATE_CONNECTED)
    		tgDevice.connect(rawEnabled);   
    	//tgDevice.ena
    }

    public void sendData(String data, String url){

        HttpClient httpClient = new DefaultHttpClient();

        try {
            HttpPost request = new HttpPost(url);

            StringEntity se = new StringEntity("details={\"data\":\""+data+"\"}");
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