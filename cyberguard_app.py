import re
import secrets
import string

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.spinner import Spinner


# ==========================================
# HOME SCREEN
# ==========================================

class HomeScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(25),
            spacing=dp(12)
        )

        title = Label(
            text="CYBERGUARD",
            font_size=dp(30),
            bold=True,
            size_hint_y=None,
            height=dp(60)
        )

        subtitle = Label(
            text="Cybersecurity Learning App",
            font_size=dp(18),
            size_hint_y=None,
            height=dp(45)
        )

        description = Label(
            text=(
                "Learn basic password security,\n"
                "generate strong passwords,\n"
                "and improve your cybersecurity knowledge."
            ),
            font_size=dp(15)
        )

        buttons = [
            ("PASSWORD CHECKER", "checker"),
            ("PASSWORD GENERATOR", "generator"),
            ("CYBERSECURITY LESSONS", "lessons"),
            ("ABOUT PROJECT", "about")
        ]

        for text, screen_name in buttons:

            button = Button(
                text=text,
                font_size=dp(16),
                size_hint_y=None,
                height=dp(55)
            )

            button.bind(
                on_press=lambda x, name=screen_name:
                self.go_to(name)
            )

            layout.add_widget(button)

        self.add_widget(layout)

    def go_to(self, screen_name):
        self.manager.current = screen_name


# ==========================================
# PASSWORD CHECKER
# ==========================================

class CheckerScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(10)
        )

        title = Label(
            text="PASSWORD SECURITY CHECKER",
            font_size=dp(23),
            bold=True,
            size_hint_y=None,
            height=dp(55)
        )

        self.password = TextInput(
            hint_text="Enter a TEST password",
            password=True,
            multiline=False,
            font_size=dp(17),
            size_hint_y=None,
            height=dp(55)
        )

        buttons = BoxLayout(
            spacing=dp(8),
            size_hint_y=None,
            height=dp(52)
        )

        check = Button(
            text="CHECK"
        )

        show = Button(
            text="SHOW"
        )

        clear = Button(
            text="CLEAR"
        )

        check.bind(
            on_press=self.check_password
        )

        show.bind(
            on_press=self.show_password
        )

        clear.bind(
            on_press=self.clear
        )

        buttons.add_widget(check)
        buttons.add_widget(show)
        buttons.add_widget(clear)

        self.result = Label(
            text="Security Score: --",
            font_size=dp(19),
            bold=True,
            size_hint_y=None,
            height=dp(70)
        )

        self.progress = ProgressBar(
            max=10,
            value=0,
            size_hint_y=None,
            height=dp(12)
        )

        self.details = Label(
            text="Enter a test password and press CHECK.",
            font_size=dp(14),
            halign="left",
            valign="top"
        )

        back = Button(
            text="BACK TO HOME",
            size_hint_y=None,
            height=dp(48)
        )

        back.bind(
            on_press=lambda x:
            setattr(
                self.manager,
                "current",
                "home"
            )
        )

        layout.add_widget(title)
        layout.add_widget(self.password)
        layout.add_widget(buttons)
        layout.add_widget(self.result)
        layout.add_widget(self.progress)
        layout.add_widget(self.details)
        layout.add_widget(back)

        self.add_widget(layout)

    def show_password(self, button):

        self.password.password = not self.password.password

        button.text = (
            "HIDE"
            if not self.password.password
            else "SHOW"
        )

    def clear(self, button):

        self.password.text = ""
        self.password.password = True

        self.result.text = "Security Score: --"
        self.progress.value = 0

        self.details.text = (
            "Enter a test password and press CHECK."
        )

    def check_password(self, button):

        password = self.password.text

        if not password:

            self.result.text = (
                "Please enter a test password."
            )

            self.progress.value = 0
            return

        score = 0
        warnings = []

        # --------------------------------
        # LENGTH
        # --------------------------------

        length = len(password)

        if length >= 16:
            score += 3
        elif length >= 12:
            score += 2
        elif length >= 8:
            score += 1
        else:
            warnings.append(
                "Use at least 8 characters."
            )

        # --------------------------------
        # LOWERCASE
        # --------------------------------

        if re.search(r"[a-z]", password):

            score += 1

        else:

            warnings.append(
                "Add lowercase letters."
            )

        # --------------------------------
        # UPPERCASE
        # --------------------------------

        if re.search(r"[A-Z]", password):

            score += 1

        else:

            warnings.append(
                "Add uppercase letters."
            )

        # --------------------------------
        # NUMBERS
        # --------------------------------

        if re.search(r"[0-9]", password):

            score += 1

        else:

            warnings.append(
                "Add numbers."
            )

        # --------------------------------
        # SPECIAL CHARACTERS
        # --------------------------------

        if re.search(
            r"[^A-Za-z0-9]",
            password
        ):

            score += 1

        else:

            warnings.append(
                "Add special characters."
            )

        # --------------------------------
        # REPEATED CHARACTERS
        # --------------------------------

        if re.search(
            r"(.)\1\1",
            password
        ):

            score -= 1

            warnings.append(
                "Avoid repeating the same character three or more times."
            )

        # --------------------------------
        # SEQUENTIAL NUMBERS
        # --------------------------------

        sequences = [
            "1234",
            "2345",
            "3456",
            "4567",
            "5678",
            "6789",
            "9876",
            "8765",
            "7654",
            "6543"
        ]

        found_sequence = False

        for sequence in sequences:

            if sequence in password:

                found_sequence = True
                break

        if found_sequence:

            score -= 1

            warnings.append(
                "Avoid predictable number sequences."
            )

        # --------------------------------
        # COMMON PASSWORDS
        # --------------------------------

        common = {
            "password",
            "password123",
            "123456",
            "12345678",
            "123456789",
            "1234567890",
            "qwerty",
            "admin",
            "letmein",
            "welcome"
        }

        if password.lower() in common:

            score = 0

            warnings.append(
                "This is a commonly used password."
            )

        # Keep score inside range
        score = max(0, min(score, 10))

        # --------------------------------
        # STRENGTH
        # --------------------------------

        if score <= 2:

            strength = "WEAK"

        elif score <= 4:

            strength = "FAIR"

        elif score <= 6:

            strength = "MEDIUM"

        elif score <= 8:

            strength = "STRONG"

        else:

            strength = "VERY STRONG"

        self.result.text = (
            f"Strength: {strength}\n"
            f"Security Score: {score}/10"
        )

        self.progress.value = score

        # --------------------------------
        # DETAILS
        # --------------------------------

        details = (
            f"Password length: {length}\n\n"
        )

        if warnings:

            details += "Security recommendations:\n\n"

            for warning in warnings:

                details += "• " + warning + "\n"

        else:

            details += (
                "No basic weaknesses detected.\n\n"
                "Remember: this checker is an educational "
                "tool and does not guarantee that a password "
                "is impossible to guess."
            )

        self.details.text = details


# ==========================================
# PASSWORD GENERATOR
# ==========================================

class GeneratorScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(25),
            spacing=dp(15)
        )

        title = Label(
            text="SECURE PASSWORD GENERATOR",
            font_size=dp(23),
            bold=True,
            size_hint_y=None,
            height=dp(60)
        )

        length_label = Label(
            text="Choose password length:",
            font_size=dp(16),
            size_hint_y=None,
            height=dp(35)
        )

        self.length_spinner = Spinner(
            text="16",
            values=[
                "12",
                "16",
                "20",
                "24",
                "32"
            ],
            size_hint_y=None,
            height=dp(50)
        )

        self.output = TextInput(
            text="Your generated password will appear here.",
            multiline=False,
            readonly=True,
            font_size=dp(16),
            size_hint_y=None,
            height=dp(60)
        )

        generate = Button(
            text="GENERATE PASSWORD",
            font_size=dp(16),
            size_hint_y=None,
            height=dp(58)
        )

        generate.bind(
            on_press=self.generate
        )

        back = Button(
            text="BACK TO HOME",
            size_hint_y=None,
            height=dp(48)
        )

        back.bind(
            on_press=lambda x:
            setattr(
                self.manager,
                "current",
                "home"
            )
        )

        layout.add_widget(title)
        layout.add_widget(length_label)
        layout.add_widget(self.length_spinner)
        layout.add_widget(self.output)
        layout.add_widget(generate)

        layout.add_widget(
            Label(
                text=(
                    "Generated passwords are created "
                    "locally and are not saved by this app."
                ),
                font_size=dp(14)
            )
        )

        layout.add_widget(back)

        self.add_widget(layout)

    def generate(self, button):

        length = int(
            self.length_spinner.text
        )

        characters = (
            string.ascii_letters
            + string.digits
            + "!@#$%^&*()-_=+"
        )

        password = "".join(
            secrets.choice(characters)
            for _ in range(length)
        )

        self.output.text = password


# ==========================================
# CYBERSECURITY LESSONS
# ==========================================

class LessonsScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(12)
        )

        title = Label(
            text="CYBERSECURITY LESSONS",
            font_size=dp(24),
            bold=True,
            size_hint_y=None,
            height=dp(55)
        )

        lessons = Label(
            text=(
                "PASSWORD SECURITY\n"
                "Use long, unique passwords and "
                "avoid reusing the same password.\n\n"

                "TWO-FACTOR AUTHENTICATION\n"
                "Use an additional authentication factor "
                "when a service supports it.\n\n"

                "PHISHING\n"
                "Be cautious with unexpected links, "
                "attachments and login requests.\n\n"

                "SOFTWARE UPDATES\n"
                "Keep your operating system and applications "
                "updated to receive security fixes.\n\n"

                "SOCIAL ENGINEERING\n"
                "Attackers may manipulate people into "
                "revealing information or performing actions."
            ),
            font_size=dp(15),
            halign="left",
            valign="top"
        )

        back = Button(
            text="BACK TO HOME",
            size_hint_y=None,
            height=dp(50)
        )

        back.bind(
            on_press=lambda x:
            setattr(
                self.manager,
                "current",
                "home"
            )
        )

        layout.add_widget(title)
        layout.add_widget(lessons)
        layout.add_widget(back)

        self.add_widget(layout)


# ==========================================
# ABOUT
# ==========================================

class AboutScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(25),
            spacing=dp(15)
        )

        title = Label(
            text="ABOUT CYBERGUARD",
            font_size=dp(24),
            bold=True,
            size_hint_y=None,
            height=dp(60)
        )

        information = Label(
            text=(
                "Project: CyberGuard\n\n"
                "Type: Cybersecurity Education App\n\n"
                "Technology: Python + Kivy\n\n"
                "Purpose:\n"
                "To demonstrate basic password security "
                "concepts and provide educational tools "
                "for cybersecurity students.\n\n"
                "Features:\n"
                "• Password strength analysis\n"
                "• Password generation\n"
                "• Security recommendations\n"
                "• Cybersecurity lessons\n"
                "• Local processing"
            ),
            font_size=dp(15)
        )

        back = Button(
            text="BACK TO HOME",
            size_hint_y=None,
            height=dp(50)
        )

        back.bind(
            on_press=lambda x:
            setattr(
                self.manager,
                "current",
                "home"
            )
        )

        layout.add_widget(title)
        layout.add_widget(information)
        layout.add_widget(back)

        self.add_widget(layout)


# ==========================================
# MAIN APPLICATION
# ==========================================

class CyberGuardApp(App):

    def build(self):

        manager = ScreenManager()

        manager.add_widget(
            HomeScreen(name="home")
        )

        manager.add_widget(
            CheckerScreen(name="checker")
        )

        manager.add_widget(
            GeneratorScreen(name="generator")
        )

        manager.add_widget(
            LessonsScreen(name="lessons")
        )

        manager.add_widget(
            AboutScreen(name="about")
        )

        return manager


CyberGuardApp().run()