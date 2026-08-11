import random

class Character:

    def __init__(self, name, health, attack_power, defense, speed):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.defense = defense
        self.speed = speed

    def take_damage(self, amount):
        damage = max(1, amount - self.defense)

        self.health -= damage

        if self.health < 0:
            self.health = 0

        return damage

    def is_alive(self):
        return self.health > 0

    def attack(self, target):
        damage = target.take_damage(self.attack_power)

        print( self.name,"attacks",target.name,"and deals",damage,"damage.")


class Warrior(Character):

    def __init__(self, name, health, attack_power, defense, speed):
        super().__init__(name,health,attack_power,defense,speed)

        self.rage = 0

    def attack(self, target):

        if self.health < 0.30 * self.max_health:

            raw_damage = self.attack_power * 2

            print(
                self.name,
                "enters Berserk Mode!"
            )

        else:
            raw_damage = self.attack_power

        damage = target.take_damage(raw_damage)

        print(self.name,"attacks",target.name,"and deals",damage,"damage.")


class Mage(Character):

    def __init__(self, name, health, attack_power, defense, speed, mana):
        super().__init__( name,health,attack_power,defense,speed)

        self.mana = mana

    def attack(self, target):

        if self.mana >= 20:

            self.mana -= 20
            raw_damage = self.attack_power * 1.5

            damage = target.take_damage(raw_damage)

            # Fireball backlash
            self.health -= 5

            if self.health < 0:
                self.health = 0

            print( self.name,"casts Fireball!","Deals",damage,"damage.",self.name,"loses 5 health.")

        else:

            damage = target.take_damage(self.attack_power)

            print(self.name,"does not have enough mana.","Normal attack deals",damage,"damage.")



class Archer(Character):

    def __init__(self, name, health, attack_power, defense, speed):
        super().__init__(name,health,attack_power,defense,speed)

        self.critical_chance = 0.30

    def attack(self, target):

        value = random.random()
        if value < self.critical_chance:
            raw_damage = self.attack_power * 2

            damage = target.take_damage(raw_damage)

            print(self.name,"lands a Critical Hit!", "Deals",damage,"damage.")
        else:

            damage = target.take_damage(self.attack_power)

            print(self.name,"shoots an arrow!","Deals",damage,"damage.")


warrior = Warrior("Thor",130,22,12,6)

mage = Mage("Mge",90,30,5,8,100)

archer = Archer("Archer",100,24,7,12)

fighters = [warrior, mage, archer]


round_number = 1

while len([f for f in fighters if f.is_alive()]) > 1:

    print("\n----------------------")
    print("ROUND", round_number)
    print("----------------------")

    fighters.sort(key=lambda x: x.speed, reverse=True)

    for fighter in fighters:

        if not fighter.is_alive():
            continue

        target = None

        for opponent in fighters:

            if opponent != fighter and opponent.is_alive():
                target = opponent
                break

        if target is None:
            break

        fighter.attack(target)

        if not target.is_alive():
            print(target.name, "is defeated!")

    round_number += 1


for fighter in fighters:

    if fighter.is_alive():

        
        print(fighter.name, "wins the battle!")
