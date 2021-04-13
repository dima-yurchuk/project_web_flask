from flask import Flask, render_template, request, redirect, url_for, flash, session
from app.forms import ContactForm
import json
from app.contact_form import contact_form_bp

@contact_form_bp.route('/contact', methods=["GET", "POST"])
def contact():
    form = ContactForm()
    cookie_name = session.get("name")
    cookie_email = session.get("email")
    print(cookie_email,cookie_name)
    if request.method == 'POST':
        if cookie_name is None and cookie_email is None: # якщо кукі не встановлено, тобто ми перший раз відкрили сторінку
            if form.validate_on_submit():
                name = form.name.data
                email = form.email.data
                body = form.body.data
                session['name'] = name
                session['email'] = email
                with open('data.json', 'a') as outfile:
                    json_string = json.dumps({'name': session.get("name"), 'email': session.get("email"), 'body': body})
                    json.dump(json_string, outfile)
                    outfile.write('\n')
                flash(message='Повідомлення надіслано успішно!')
                return redirect(url_for('contact_form_bp_in.contact'))
            else:
                flash(message='Помилка відправки повідомлення!')
        else: # якщо вхід на сторіку здійснено повторно
            form.name.data = cookie_name # встановлюємо значення для форми name та email
            form.email.data = cookie_email
            if form.validate_on_submit():
                body = form.body.data
                with open('data.json', 'a') as outfile:
                    json.dump({'name': session.get("name"), 'email': session.get("email"), 'body': body}, outfile)
                    outfile.write('\n')
                flash(message='Повідомлення надіслано успішно!')
                return redirect(url_for('contact_form_bp_in.contact'))
            else:
                flash(message='Помилка відправки повідомлення!')
    return render_template('contact_form.html', form=form, cookie_name=session.get("name"), cookie_email=session.get("email"))