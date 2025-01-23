from app.schemas.language_content import LanguageContent
from fastapi import HTTPException


class LanguageService:
    def __init__(self):
        self.language_content = {
            "english": {
                "modules": [
                    {
                        "module_id": 1,
                        "name": "Basics",
                        "levels": [
                            {
                                "level_id": 1,
                                "name": "Level 1",
                                "lessons": [
                                    {
                                        "lesson_id": 1,
                                        "name": "Greetings",
                                        "icon": "waving_hand",
                                        "exercises": [
                                            {
                                                "exercise_id": 1,
                                                "type": "multiple_choice",
                                                "question": "Select the greeting",
                                                "options": [
                                                    {
                                                        "text": "Hello",
                                                        "icon": "waving-hand",
                                                        "icon_color": "#FFCC00",
                                                        "iconType": "FontAwesome5"
                                                    },
                                                    {
                                                        "text": "Goodbye",
                                                        "icon": "farewell",
                                                        "icon_color": "#FF5722",
                                                        "iconType": "FontAwesome5"
                                                    },
                                                    {
                                                        "text": "Thanks",
                                                        "icon": "hand-thumbs-up",
                                                        "icon_color": "#4CAF50",
                                                        "iconType": "FontAwesome5"
                                                    },
                                                ],
                                                "correct_option": "Hello",
                                            },
                                            {
                                                "exercise_id": 2,
                                                "type": "translate",
                                                "question": "Translate 'Hello'",
                                                "correct_answer": "Hola",
                                            },
                                        ],
                                    },
                                    {
                                        "lesson_id": 2,
                                        "name": "Introductions",
                                        "icon": "diversity-3",
                                        "exercises": [
                                            {
                                                "exercise_id": 3,
                                                "type": "multiple_choice",
                                                "question": "How do you introduce yourself?",
                                                "options": [
                                                    {
                                                        "text": "My name is",
                                                        "icon": "user",
                                                        "icon_color": "#00BFFF",
                                                        "iconType": "FontAwesome5"
                                                    },
                                                    {
                                                        "text": "I am",
                                                        "icon": "user-circle",
                                                        "icon_color": "#FF5722",
                                                        "iconType": "FontAwesome5"
                                                    },
                                                    {
                                                        "text": "Hello, my name is",
                                                        "icon": "handshake",
                                                        "icon_color": "#FFCC00",
                                                        "iconType": "FontAwesome5"
                                                    },
                                                ],
                                                "correct_option": "My name is",
                                            },
                                            {
                                                "exercise_id": 4,
                                                "type": "translate",
                                                "question": "Translate 'My name is John'",
                                                "correct_answer": "Mi nombre es John",
                                            },
                                        ],
                                    },
                                ],
                            }
                        ],
                    }
                ]
            },
            "spanish": {
                "modules": [
                    {
                        "module_id": 1,
                        "name": "Fundamentals",
                        "levels": [
                            {
                                "level_id": 1,
                                "name": "Nivel 1",
                                "lessons": [
                                    {
                                        "lesson_id": 1,
                                        "name": "Saludos",
                                        "icon": "waving-hand",
                                        "exercises": [
                                            {
                                                "exercise_id": 1,
                                                "type": "multiple_choice",
                                                "question": "Which of these is a hive",
                                                "options": [
                                                    {
                                                        "text": "Hola",
                                                        "icon": "waving-hand",
                                                        "icon_color": "#FFCC00",
                                                        "iconType": "MaterialIcons"
                                                    },
                                                    {
                                                        "text": "Pensar",
                                                        "icon": "brain",
                                                        "icon_color": "#00BFFF",
                                                        "iconType": "MaterialCommunityIcons"
                                                    },
                                                    {
                                                        "text": "Jugar",
                                                        "icon": "gamepad",
                                                        "icon_color": "#4CAF50",
                                                        "iconType": "FontAwesome5"
                                                    },
                                                    {
                                                        "text": "Colmena",
                                                        "icon": "hive",
                                                        "icon_color": "#FF5722",
                                                        "iconType": "MaterialIcons"
                                                    }
                                                ],
                                                "correct_option": "Colmena",
                                            },
                                            {
                                                "exercise_id": 2,
                                                "type": "translate",
                                                "question": "Translate 'Goodbye'",
                                                "correct_answer": "Adiós",
                                            },
                                            {
                                                "exercise_id": 3,
                                                "type": "multiple_choice",
                                                "question": "What is the capital of France?",
                                                "options": [
                                                    {
                                                        "text": "Berlin",
                                                        "icon": "landmark",
                                                        "icon_color": "#FF5722",
                                                        "iconType": "FontAwesome5"
                                                    },
                                                    {
                                                        "text": "Madrid",
                                                        "icon": "building",
                                                        "icon_color": "#4CAF50",
                                                        "iconType": "FontAwesome5"
                                                    },
                                                    {
                                                        "text": "Paris",
                                                        "icon": "eiffel-tower",
                                                        "icon_color": "#FFCC00",
                                                        "iconType": "FontAwesome5"
                                                    },
                                                    {
                                                        "text": "Rome",
                                                        "icon": "colosseum",
                                                        "icon_color": "#00BFFF",
                                                        "iconType": "FontAwesome5"
                                                    }
                                                ],
                                                "correct_option": "Paris",
                                            },
                                            {
                                                "exercise_id": 4,
                                                "type": "fill_in_the_blank",
                                                "question": "The Eiffel Tower is located in _______",
                                                "correct_answer": "Paris",
                                            },
                                            {
                                                "exercise_id": 5,
                                                "type": "microphone",
                                                "question": "Listen and repeat the word 'Water'",
                                                "audio_url": "https://example.com/audio/water.mp3",
                                                "correct_answer": "Water",
                                            },
                                            {
                                                "exercise_id": 6,
                                                "type": "multiple_choice",
                                                "question": "Which one is a fruit?",
                                                "options": [
                                                    {
                                                        "text": "Carrot",
                                                        "icon": "carrot",
                                                        "icon_color": "#FF5722",
                                                        "iconType": "FontAwesome5"
                                                    },
                                                    {
                                                        "text": "Apple",
                                                        "icon": "apple-alt",
                                                        "icon_color": "#FFCC00",
                                                        "iconType": "FontAwesome5"
                                                    },
                                                    {
                                                        "text": "Potato",
                                                        "icon": "potato",
                                                        "icon_color": "#4CAF50",
                                                        "iconType": "FontAwesome5"
                                                    },
                                                    {
                                                        "text": "Onion",
                                                        "icon": "lemon",
                                                        "icon_color": "#00BFFF",
                                                        "iconType": "FontAwesome5"
                                                    }
                                                ],
                                                "correct_option": "Apple",
                                            },
                                        ]
                                    }
                                ],
                            }
                        ],
                    }
                ]
            },
            "french": {
                "modules": [
                    {
                        "module_id": 1,
                        "name": "Basics",
                        "levels": [
                            {
                                "level_id": 1,
                                "name": "Niveau 1",
                                "lessons": [
                                    {
                                        "lesson_id": 1,
                                        "name": "Salutations",
                                        "icon": "waving-hand",
                                        "exercises": [
                                            {
                                                "exercise_id": 1,
                                                "type": "multiple_choice",
                                                "question": "Quel est le salut en français?",
                                                "options": [
                                                    {
                                                        "text": "Bonjour",
                                                        "icon": "hand-wave",
                                                        "icon_color": "#FFCC00",
                                                        "iconType": "FontAwesome5"
                                                    },
                                                    {
                                                        "text": "Au revoir",
                                                        "icon": "hand-paper",
                                                        "icon_color": "#FF5722",
                                                        "iconType": "FontAwesome5"
                                                    },
                                                    {
                                                        "text": "Merci",
                                                        "icon": "hands-clapping",
                                                        "icon_color": "#4CAF50",
                                                        "iconType": "FontAwesome5"
                                                    },
                                                ],
                                                "correct_option": "Bonjour",
                                            },
                                            {
                                                "exercise_id": 2,
                                                "type": "translate",
                                                "question": "Translate 'Good morning'",
                                                "correct_answer": "Bonjour",
                                            },
                                        ],
                                    },
                                    {
                                        "lesson_id": 2,
                                        "name": "Introductions",
                                        "icon": "diversity-3",
                                        "exercises": [
                                            {
                                                "exercise_id": 3,
                                                "type": "multiple_choice",
                                                "question": "Comment vous présentez-vous?",
                                                "options": [
                                                    {
                                                        "text": "Je m'appelle",
                                                        "icon": "user",
                                                        "icon_color": "#00BFFF",
                                                        "iconType": "FontAwesome5"
                                                    },
                                                    {
                                                        "text": "Je suis",
                                                        "icon": "user-circle",
                                                        "icon_color": "#FF5722",
                                                        "iconType": "FontAwesome5"
                                                    },
                                                    {
                                                        "text": "Bonjour, je m'appelle",
                                                        "icon": "handshake",
                                                        "icon_color": "#FFCC00",
                                                        "iconType": "FontAwesome5"
                                                    },
                                                ],
                                                "correct_option": "Je m'appelle",
                                            },
                                            {
                                                "exercise_id": 4,
                                                "type": "translate",
                                                "question": "Translate 'My name is Marie'",
                                                "correct_answer": "Je m'appelle Marie",
                                            },
                                        ],
                                    },
                                ],
                            }
                        ],
                    }
                ]
            },
        }

    async def get_language_content(self, language: str) -> LanguageContent:
        """Obtiene el contenido de un idioma completo, con módulos, niveles, lecciones y ejercicios."""
        if language not in self.language_content:
            raise HTTPException(
                status_code=404, detail=f"Language {language} not found"
            )
        return self.language_content[language]
