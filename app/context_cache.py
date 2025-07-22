
# app/context_cache.py
context_store = {}

def get_context(chat_id):
    return context_store.get(chat_id, [])

def add_to_context(chat_id, user_input, bot_response):
    if chat_id not in context_store:
        context_store[chat_id] = []
    context_store[chat_id].append((user_input, bot_response))
    # limitar histórico a 5 interações para não pesar
    context_store[chat_id] = context_store[chat_id][-5:]
