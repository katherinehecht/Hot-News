package com.katherinehecht.hotnews;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends AppCompatActivity {

    private WebView myView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        myView = (WebView) findViewById(R.id.webView);
        WebSettings webSettings = myView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        myView.loadUrl("http://student04.cse.nd.edu/khecht/paradigms/floodFill.html");
        myView.setWebViewClient(new WebViewClient());

    }

    @Override
    public void onBackPressed() {
        if(myView.canGoBack()){
            myView.goBack();
        }else {
            super.onBackPressed();
        }
    }



}
