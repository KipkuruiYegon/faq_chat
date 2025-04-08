from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse
from .openai_utils import find_best_faq, get_gpt_response

# 🌐 Web-based FAQ chatbot (form-based)
def home(request):
    answer = None

    if request.method == 'POST':
        user_question = request.POST.get('question')
        if user_question:
            faq = find_best_faq(user_question)
            if faq:
                answer = get_gpt_response(user_question, faq)
            else:
                answer = "Sorry, I couldn’t find an answer for that question."

    return render(request, 'index.html', {"answer": answer})


# 📲 WhatsApp-based chatbot (Twilio)
@csrf_exempt
def whatsapp_webhook(request):
    if request.method == "POST":
        user_msg = request.POST.get("Body", "").strip()

        faq = find_best_faq(user_msg)
        if faq:
            reply = get_gpt_response(user_msg, faq)
        else:
            reply = "Sorry, I couldn’t find an answer. Want me to connect you to support?"

        resp = MessagingResponse()
        resp.message(reply)
        return HttpResponse(str(resp), content_type="text/xml")

    return HttpResponse("Not allowed", status=405)
