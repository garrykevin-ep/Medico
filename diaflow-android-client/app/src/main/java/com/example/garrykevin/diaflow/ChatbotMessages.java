package com.example.garrykevin.diaflow;

import android.support.v7.app.AppCompatActivity;

import com.example.garrykevin.diaflow.models.Message;
import com.stfalcon.chatkit.messages.MessagesListAdapter;

/**
 * Created by garrykevin on 9/6/18.
 */

public class ChatbotMessages extends AppCompatActivity implements MessagesListAdapter.SelectionListener,
        MessagesListAdapter.OnLoadMoreListener {

    protected final String senderId = "0";
    protected MessagesListAdapter<Message> messagesAdapter;

    @Override
    public void onLoadMore(int page, int totalItemsCount) {

    }

    @Override
    public void onSelectionChanged(int count) {

    }
}
