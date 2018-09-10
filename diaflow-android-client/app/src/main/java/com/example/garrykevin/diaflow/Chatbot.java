package com.example.garrykevin.diaflow;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;

import com.example.garrykevin.diaflow.models.Message;
import com.example.garrykevin.diaflow.models.User;
import com.stfalcon.chatkit.commons.models.IMessage;
import com.stfalcon.chatkit.commons.models.IUser;
import com.stfalcon.chatkit.messages.MessageInput;
import com.stfalcon.chatkit.messages.MessagesList;
import com.stfalcon.chatkit.messages.MessagesListAdapter;

import java.security.SecureRandom;
import java.util.Date;
import java.util.UUID;

import ai.api.AIListener;
import ai.api.android.AIConfiguration;
import ai.api.android.AIService;
import ai.api.model.AIError;
import ai.api.model.AIResponse;
import ai.api.model.Fulfillment;
import ai.api.model.Result;

public class Chatbot extends AppCompatActivity implements MessageInput.InputListener,AIListener {

    protected static String senderId = "0";
    protected static String receiverId = "1";
    protected MessagesListAdapter<Message> messagesAdapter;
    static SecureRandom rnd = new SecureRandom();
    private MessagesList messagesList;
    private AIService aiService;

    static String getRandomId() {
        return Long.toString(UUID.randomUUID().getLeastSignificantBits());
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chatbot);
        this.messagesList = (MessagesList) findViewById(R.id.messagesList);
        initAdapter();

        final AIConfiguration config = new AIConfiguration("c4b3618cebd04d09919236cf0de4e017",
                AIConfiguration.SupportedLanguages.English,
                AIConfiguration.RecognitionEngine.System);

        aiService = AIService.getService(this, config);
        aiService.setListener(this);

//        MessageInput input = (MessageInput) findViewById(R.id.input);
//        input.setInputListener(this);
//        input.setTypingListener(this);
//        input.setAttachmentsListener(this);

    }

    private void initAdapter() {
        messagesAdapter = new MessagesListAdapter<>(senderId, null);
//        messagesAdapter.enableSelectionMode(this);
//        messagesAdapter.setLoadMoreListener(this);
        this.messagesList.setAdapter(messagesAdapter);
    }


    @Override
    public boolean onSubmit(CharSequence input) {
//        messagesAdapter.addToStart(new Message("1",getUser(),input.toString()),true);
        messagesAdapter.addToStart(new Message("0",getSender(),input.toString()+" sender"),true);
        return true;
    }

    public void senderMessage(String input)
    {
        messagesAdapter.addToStart(new Message(getRandomId(),getSender(),input),true);
    }

    public void receiverMessage(String input)
    {
        messagesAdapter.addToStart(new Message(getRandomId(),getReceiver(),input),true);
    }

    private  User getReceiver() {

        return new User(receiverId,"kevin","none",true);
    }

    private User getSender() {

        return new User(senderId,"sender","none",true);
    }

    public void listenButtonOnClick(final View view) {
//        messagesAdapter.addToStart(new Message("0",getsender(),"sender"),true);
        aiService.startListening();
    }

    @Override
    public void onResult(final AIResponse response) {
        Result result = response.getResult();
        Fulfillment fulfillment =  result.getFulfillment();
        String sendMessageText = result.getResolvedQuery();
        String receivedMessageText = fulfillment.getSpeech();
        senderMessage(sendMessageText);
        receiverMessage(receivedMessageText);
//        Log.d("display text",recivedMessageText);
    }

    @Override
    public void onError(AIError error) {

    }

    @Override
    public void onAudioLevel(float level) {

    }

    @Override
    public void onListeningStarted() {

    }

    @Override
    public void onListeningCanceled() {

    }

    @Override
    public void onListeningFinished() {

    }
}
