from mugloarWebClient import MugloarWebClient
from const.mugloarProbability import *
from const.mugloarItems import *
import base64


class Game:
    mwc = MugloarWebClient()
    games_played = 0
    games_won = 0
    score_history = []

    game_state = {
        # internal game stuff
        "gameId": "",
        "turn": 0,

        # Player stats:
        "lives": 0,
        "gold": 0,
        "level": 0,
        "score": 0,
        "highScore": 0,
        "turn": 0,

        # Player reputation
        "reputation_people": 0,
        "reputation_state": 0,
        "reputation_underworld": 0
    }

    items_bought = []

    def __init__(self):
        self.start()
    
    def start(self):
        print("Welcome to Dragons of Mugloar!\n The game will be played automatically for you so sit back and relax. There will be 10 rounds. Hopefully our knight in shining armour will win all ten of these games.")
        input("Enter any key to start the game...")
        while self.games_played < 100:
            self.game_state.update(self.mwc.startNewGame())
            self.auto_run_game()

            # Save stats:
            self.score_history += [self.game_state["score"]]
            self.games_played += 1
            if self.game_state["score"] >= 1000:
                self.games_won += 1
        print("The game has finished. Our knight won " + str(self.games_won) + " out of " + str(self.games_played) + " games. Well done regardless!")
        print(self.score_history)

    def auto_run_game(self):
        while(self.game_state["lives"] != 0):
            #print("lives left:" + str(self.game_state["lives"]))
            self.solve_safest_ad()
            self.check_for_items()
            if self.game_state["score"] >= 1000:
                return
        
        # save scores in a a file
        #self.save_score()
                    
    def check_for_items(self):
        # Could player die next fight?
        if self.game_state["lives"] <= 1:
            self.purchase_item(HEALTH_POT, 50)
        
        self.purchase_item(CLAW_SHARPENING, 100)
        self.purchase_item(BOOK_OF_TRICKS, 100)
        self.purchase_item(POTION_OF_STRONGER_WINGS, 100)
        self.purchase_item(COPPER_PLATING, 100)
        self.purchase_item(GASOLINE, 100)
        self.purchase_item(BOOK_OF_MEGATRICKS, 300)
        self.purchase_item(CLAW_HONING, 300)
        self.purchase_item(ROCKET_FUEL, 300)
        self.purchase_item(IRON_PLATING, 300)
        self.purchase_item(POTION_OF_AWESOME_WINGS, 300)

        if self.game_state["gold"] > 600:
            print("Purchasing " + CLAW_HONING + "!")
            message = self.mwc.purchaseShopItem(self.game_state["gameId"], CLAW_HONING)
            self.game_state.update((k, v) for k, v in message.items() if k in self.game_state)

    def purchase_item(self, item, gold_reserve):
        # do not purchase the item if there is not enough gold in the reserve
        if self.game_state["gold"] >= gold_reserve and item not in self.items_bought:
            print("Purchasing " + item + "!")
            message = self.mwc.purchaseShopItem(self.game_state["gameId"], item)
            self.game_state.update((k, v) for k, v in message.items() if k in self.game_state)

            if item is not HEALTH_POT:
                self.items_bought += [item]

    def solve_safest_ad(self):
        ads = self.mwc.getAllMessages(self.game_state["gameId"])

        chosen_ad = {"reward": -999, "probability": IMPOSSIBLE, "expiresIn": -1}
        for ad in ads:
            if("encrypted" in ad):
                ad = self.decrypt(ad)

            if(risk_factor[chosen_ad["probability"]] > risk_factor[ad["probability"]] 
            or (risk_factor[chosen_ad["probability"]] >= risk_factor[ad["probability"]] and chosen_ad["expiresIn"] < ad["expiresIn"])
            #or (risk_factor[chosen_ad["probability"]] == risk_factor[ad["probability"]] and chosen_ad["reward"] < ad["reward"])
            #and chosen_ad["expiresIn"] >= ad["expiresIn"]
            ):
                chosen_ad = ad
        #print("Ad chosen: " + str(chosen_ad))
        solve_message = self.mwc.solveMessage(self.game_state["gameId"], chosen_ad["adId"])
        self.game_state.update((k, v) for k, v in solve_message.items() if k in self.game_state)
        print(solve_message)

    def save_score(self):
        score = str(self.game_state["score"])
        print("Game ended with score " + score)
        if(self.game_state["lives"] == 0):
            f = open("game.score.txt", "a")
            f.write(str(self.game_state["score"]) + "\n")
            f.close()

    def decrypt(self, ad):
        if (ad["encrypted"] == 1):
            ad["adId"] = base64.b64decode(ad["adId"]).decode('UTF-8')
            ad["message"] = base64.b64decode(ad["message"]).decode('UTF-8')
            ad["probability"] = base64.b64decode(ad["probability"]).decode('UTF-8')
        elif (ad["encrypted"] == 2):
            caesar_cipher_step = 13
            ad["adId"] = self.caesar_cipher(ad["adId"], caesar_cipher_step)
            ad["message"] = self.caesar_cipher(ad["message"], caesar_cipher_step)
            ad["probability"] = self.caesar_cipher(ad["probability"], caesar_cipher_step)
        return ad

    def caesar_cipher(self, text, step):
        alpha_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        alpha = "abcdefghijklmnopqrstuvwxyz"
        result = ""

        for letter in text:
            if(letter in alpha_upper):
                letter_index = (alpha_upper.find(letter) - step) % len(alpha_upper)
                result = result + alpha_upper[letter_index] 
            elif(letter in alpha):
                letter_index = (alpha.find(letter) - step) % len(alpha)
                result = result + alpha[letter_index] 
            else: # when letter is a symbol
                result = result + letter
        return result