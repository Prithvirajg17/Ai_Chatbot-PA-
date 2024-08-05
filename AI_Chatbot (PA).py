import gradio as gr
import openai
import random
import time

# Configure OpenAI API key
openai.api_key = "Enter your API Key here"

assistant_preset = {"role": "system", "content": "You are a helpful assistant."}

with gr.Blocks() as app:
    conversation_interface = gr.Chatbot()
    input_box = gr.Textbox()
    reset_button = gr.Button("Reset")

    history_state = gr.State([])

    def user_input(user_text, conversation_history):
        return "", conversation_history + [[user_text, None]]

    def assistant_response(conversation_history, message_log):
        user_text = conversation_history[-1][0]
        reply_text, message_log = generate_reply(user_text, message_log)
        message_log.append({"role": "assistant", "content": reply_text})
        conversation_history[-1][1] = reply_text
        time.sleep(1)
        return conversation_history, message_log

    def generate_reply(user_text, message_log):
        message_log.append({"role": "user", "content": user_text})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message_log
        )
        return response['choices'][0]['message']['content'], message_log

    def reset_history(message_log):
        message_log = [assistant_preset]
        return message_log

    input_box.submit(user_input, [input_box, conversation_interface], [input_box, conversation_interface], queue=False).then(
        assistant_response, [conversation_interface, history_state], [conversation_interface, history_state]
    )

    reset_button.click(lambda: None, None, conversation_interface, queue=False).success(reset_history, [history_state], [history_state])

app.launch()
