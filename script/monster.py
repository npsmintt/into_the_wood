import json


class Monster:
    def __init__(self, name, description, health, attack, loot, items_required, hint, bonus, words):
        self.name = name
        self.description = description
        self.health = health
        self.attack = attack
        self.loot = loot
        self.items_required = items_required
        self.hint = hint
        self.bonus = bonus
        self.words = words
    #Replacing the word based on the character information
    def replace_word(self, username, character_name):
        hair_color = self.get_hair_color(username, character_name)
        eye_color = self.get_eye_color(username, character_name)

        replaced_words = self.words
        if hair_color:
            replaced_words = replaced_words.replace("{hair_color}", hair_color)
        if eye_color:
            replaced_words = replaced_words.replace("{eye_color}", eye_color)
        replaced_words = replaced_words.replace("{character_name}", character_name)

        return replaced_words if hair_color or eye_color else "Unknown character."

    def get_hair_color(self, username, character_name):
        try:
            with open('users.json', 'r') as file:
                users_data = json.load(file)
        except IOError:
            print("[deep_pink2](⋟﹏⋞)Oops, file not found or inaccessible.[/]")
            return None

        user_data = users_data.get(username, {})
        for character in user_data.get("characters", []):
            if character.get("name") == character_name:
                return character.get('hair_color')
        return None

    def get_eye_color(self, username, character_name):
        try:
            with open('users.json', 'r') as file:
                users_data = json.load(file)
        except IOError:
            print("[deep_pink2](⋟﹏⋞)Oops, file not found or inaccessible.[/]")
            return None

        user_data = users_data.get(username, {})
        for character in user_data.get("characters", []):
            if character.get("name") == character_name:
                return character.get('eye_color')
        return None


monsters = {
    'Diet Monster':Monster('Diet Monster',
                           "The Diet Monster is created by society's push for women to be thin and the intense focus on dieting. It grows in the battle between wanting to enjoy food and needing to control it. This creature feeds on the mixed feelings and guilt about what to eat. It lives where food is both comforting and worrisome.",
                           100,
                           20,
                           'Self-Acceptance',
                           ['Pizza', 'Jumping Rope'],
                           "To defeat the Diet Monster, you need both 'Pizza' and 'Jumping Rope'. With 'Pizza' you can form a healthy relationship with food and with 'Jumping Rope' you can exercise to keep yourself fit.",
                           20,
                           "Hey, {hair_color} head, why bother trying to eat healthy? You never stick to it anyway. You don't have the willpower like others do."),
    'Insecure Monster':Monster('Insecure Monster',
                               "The Insecure Monster stays away from open fights and likes to weaken its enemies in sneaky ways. It attacks by causing doubt and feeding on the uncertainty and pause that follow. This monster isn't very strong or bold, but it's hard to face directly because it uses the deep fears of its opponents against them.",
                               100,
                               20,
                               'Courage',
                               ['Book'],
                               "To defeat the Insecure Monster, you need a 'Book'. With the 'Book' you can equip yourself with knowledge and feel secured.",
                               10,
                               "{character_name}, are you really good enough for this? Think about all the times you've failed before. Maybe you're just not cut out for success like others are."
                               ),
    'Overthinking Monster': Monster('Overthinking Monster',
                                    "This monster comes from the shared worry and stress of overthinking too much. It represents the rush of thoughts that can stop and confuse someone. It hides in the deepest parts of the mind, getting stronger from not being able to decide and from doubt.",
                                    100,
                                    20,
                                    'Serenity',
                                    ['Mirror'],
                                    "To defeat the Insecure Monster, you need a 'Mirror'. With the 'Mirror' you can have a right percetion on yourself.",
                                    10,
                                    "Look at you {character_name}, what if you make the wrong decision? You know how every little choice can go badly. It's probably safer not to decide at all."
                                    ),
    'Balance Monster': Monster('Balance Monster',
                               "The Balance Monster comes from the pressures and expectations society puts on women to be great in both their work and personal lives. It represents the struggle to find a good balance between work and life. This monster grows stronger from the stress and guilt that come from these competing demands.",
                               100,
                               20,
                               'Equality',
                               ['Smart Planner', 'Clock'],
                               "To defeat the Balance Monster, you need a 'Smart Planne' and a 'Clock'. With the 'Smart Planner' and 'Clock', you can master the work-life balance.",
                               20,
                               "I am sorry to say this, {character_name}, but you'll never get this balance right. If you focused on work, your personal life suffers, and if you relax a bit, your career falls behind. It's impossible to manage both successfully."),
    'Glass Ceiling Monster': Monster('Glass Ceiling Monster',
                                     "This monster comes from the unseen obstacles that stop women from moving forward in their careers. It symbolizes the frustration and limits of the glass ceiling. This creature gets stronger in places where inequality and unfairness are ignored.",
                                     100,
                                     20,
                                     'Empowerment',
                                     ['Key'],
                                     "To defeat the Glass Ceiling Monster, you need a 'Key'. With the 'Key', you can climb to the top of your career ladder.",
                                     20,
                                     "Hi {eye_color} eye, why strive for more when you're just going to hit the ceiling? You've seen others try and fail. It's just not meant for someone like you."),
    'Harassment Monster': Monster('Harassment Monster',
                                  "This monster stands for the widespread problem of harassment that women face in different areas of life. It becomes more powerful in places where this kind of behavior is overlooked or seen as normal.",
                                  100,
                                  20,
                                  'Strength',
                                  ['Pizza', 'Key', 'Mirror', 'Book', 'Clock'],
                                  "To defeat the Harassment Monster, you need a lot of items which will make you stronger to say no to the harassment and fight against the monster.",
                                  50,
                                  "Hey, {hair_color} head, it's just the way things are, why make a fuss? Speaking up will only make it worse for you. Better to stay quiet and not rock the boat."
                                  )

}
