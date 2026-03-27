import random
import time

# --- DATA STRUCTURES ---
# Dictionary to handle type advantages
STRENGTHS = {"Fire": "Grass", "Water": "Fire", "Grass": "Water", "Electric": "Water"}


class Pokemon:
    def __init__(self, name, p_type, hp, attack):
        self.name = name
        self.p_type = p_type
        self.hp = hp
        self.max_hp = hp
        self.attack = attack

    def __str__(self):
        return f"{self.name} ({self.p_type} Type) - HP: {self.hp}/{self.max_hp}"

    def hit(self, opponent):
        damage = self.attack

        # Type effectiveness logic
        if STRENGTHS.get(self.p_type) == opponent.p_type:
            damage *= 2
            print("💥 It's super effective!")

        opponent.hp -= damage
        if opponent.hp < 0:
            opponent.hp = 0

        print(f"{self.name} dealt {damage} damage to {opponent.name}!")


# --- GAME SETUP ---
# Creating our roster of 6 Pokemon
roster = [
    Pokemon("Charmander", "Fire", 100, 20),
    Pokemon("Squirtle", "Water", 120, 15),
    Pokemon("Bulbasaur", "Grass", 110, 18),
    Pokemon("Pikachu", "Electric", 90, 25),
    Pokemon("Vulpix", "Fire", 95, 22),
    Pokemon("Staryu", "Water", 105, 19),
]

print("--- WELCOME TO THE POKEMON ARENA ---")
for i, p in enumerate(roster):
    print(f"[{i}] {p.name} ({p.p_type} Type)")

# User picks their Pokemon
choice = int(input("\nChoose your Pokemon (0-5): "))
player = roster[choice]

# Computer picks a random opponent (excluding the one you chose)
opponent = random.choice([p for p in roster if p != player])

print(f"\nYOU CHOSE: {player}")
print(f"OPPONENT CHOSE: {opponent}")
time.sleep(1)

# --- THE BATTLE LOOP ---
potions = 3

while player.hp > 0 and opponent.hp > 0:
    print("\n" + "=" * 30)
    print(
        f"PLAYER: {player.hp}/{player.max_hp} HP | ENEMY: {opponent.hp}/{opponent.max_hp} HP"
    )
    print(f"Potions left: {potions}")
    print("=" * 30)

    print("1. Attack")
    print("2. Use Potion (+40 HP)")

    action = input("Pick an action (1 or 2): ")

    # Player Turn
    if action == "1":
        player.hit(opponent)
    elif action == "2":
        if potions > 0:
            player.hp += 40
            if player.hp > player.max_hp:
                player.hp = player.max_hp
            potions -= 1
            print(f"✨ {player.name} used a potion! HP is now {player.hp}.")
        else:
            print("❌ No potions left! You wasted your turn!")
    else:
        print("⚠️ Invalid choice! You tripped and missed your turn.")

    # Check if enemy fainted
    if opponent.hp <= 0:
        print(f"\n🎉 {opponent.name} fainted! YOU WIN!")
        break

    # Enemy Turn (AI)
    print(f"\n--- {opponent.name}'s Turn ---")
    time.sleep(1.5)
    opponent.hit(player)

    # Check if player fainted
    if player.hp <= 0:
        print(f"\n💀 {player.name} fainted! GAME OVER.")

print("\nThank you for playing!")
