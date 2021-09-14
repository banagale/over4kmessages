# application/views.py

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView

from contacts.const import (TEXT_166_KB, TEXT_71_4_KB, TEXT_23_8_KB, TEXT_4_75_KB, TEXT_3_8_KB)
from contacts.forms import ContactForm


class ContactView(FormView):
    form_class = ContactForm
    template_name = 'contacts/index.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.info(self.request, TEXT_166_KB)
        # messages.info(self.request, TEXT_71_4_KB)
        # messages.info(self.request, TEXT_23_8_KB)
        # messages.info(self.request, TEXT_4_75_KB)
        # messages.info(self.request, TEXT_3_8_KB)

        return super().form_valid(form)
