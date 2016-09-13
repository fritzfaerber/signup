#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2
import cgi
import re

page_head = """
<!DOCTYPE html>
<html>
    <head>
        <style>
            form {
                background-color: #eee;
                padding: 20px;
                margin: 0 auto;
                width: 540px;
                font: 16px sans-serif;
                border-radius: 10px;
            }
            textarea {
                margin: 10px 0;
                width: 540px;
                height: 120px;
            }
            p.error {
                color: red;
            }
        </style>
    </head>
    """

user_input = """
<body>
    <div>
        <form action="/user_info" method="POST">
            <label for="message">Username</label>
            <input type="text" name="username"/>
            <br>
            <label for="password">Password</label>
            <input type="password" name="password"/>
            <button >submit</button>
            <br>
            <label for="password">Password (confirm)</label>
            <input type="password" name="verify"/>
            <button >submit</button>
            <br>
            <label for="email">E-mail (optional)</label>
            <input type="text" name="email"/>
            <button >submit</button>
</body>
"""
class MainHandler(webapp2.RequestHandler):

    def get(self):
        user_input
        self.response.write(page_head + user_input)

class User_InfoHandler(webapp2.RequestHandler):


    def post(self):
# various error messages defined
        error_user = "<p>Enter valid Username!</p>"
        error_pass1 = "<p>You need to create a password!</p>"
        error_pass2 = "<p>Your passwords don't match!</p>"
        error_address = "<p>Please input valid e-mail address!</p>"#error message if no text is entered

        ##USERNAME CHECK--
        user_name = self.request.get("username")
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        number_errors = 0
        def valid_user_name(username):
            return USER_RE.match(username)
        if valid_user_name(user_name):
            error_user = ""
        else:
            number_errors += 1
        #PASSWORD CHECK--
        password1 = self.request.get("password")
        PASS_RE = re.compile(r"^.{3,20}$")
        def valid_password(password):
            return PASS_RE.match(password)
        if valid_password(password1):
            error_pass1 = ""
        else:
            number_errors += 1
        ## VERIFY CHECK --
        password2 = self.request.get("verify")
        if password1 == password2:
            error_pass2 = ""
        else:
            number_errors += 1
        ##EMAIL CHECK --
        email_address = self.request.get("email")
        EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]$")
        def valid_email(email):
            return EMAIL_RE.match(email)
        if valid_email(email_address):
            error_address = ""
        elif email_address == "":
            error_address = ""
        else:
            number_errors += 1

        user_input = """
        <body>
            <div>
                <form action="/user_info" method="POST">
                    <label for="message">Username{0}</label>
                    <input type="text" name="username" value="{4}"/>
                    <br>
                    <label for="password">Password{1}</label>
                    <input type="password" name="password"/>
                    <button >submit</button>
                    <br>
                    <label for="password">Password (confirm){2}</label>
                    <input type="password" name="verify"/>
                    <button >submit</button>
                    <br>
                    <label for="email">E-mail (optional){3}</label>
                    <input type="text" name="email" value="{5}"/>
                    <button >submit</button>
        </body>
        """.format(error_user, error_pass1, error_pass2, error_address, user_name, email_address)
        if number_errors == 0:
            self.response.write("Welcome " + user_name)
        else:
            self.response.write(page_head + user_input)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/user_info', User_InfoHandler)
], debug=True)
