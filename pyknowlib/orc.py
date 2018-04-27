from pyknow import *


class Personne(Fact):
    pass


class Inference(KnowledgeEngine):

    def __init__(self):
        super().__init__()
        self.chaine = ""
    @Rule()
    def personne_concernee(self):
        if self.facts[1]['age'] > 14:
            print("Cest une personne concernee par ce Systeme Expert")
            self.chaine += "Cest une personne concernee par ce Systeme Expert \n"
            self.declare(Fact(concernee=True))
        else:
            print("Cest une personne non concernee par ce Systeme Expert")
            self.chaine += "Cest une personne non concernee par ce Systeme Expert \n"
            self.declare(Fact(concernee=False))

    @Rule(Fact(concernee=True))
    def glycemie(self):
        if self.facts[1]['glycemie'] < 0.6:

            self.declare(Fact(hypoglycemie=True))
        else:

            self.declare(Fact(hypoglycemie=False))

    @Rule(Fact(concernee=True) & Fact(hypoglycemie=True) & Personne(est_consciente=True))
    def protocole_hypoglycemie(self):
        print("RESUCRAGE PER OS")
        self.chaine += "RESUCRAGE PER OS \n"

    @Rule(Fact(concernee=True) & Fact(hypoglycemie=True) & Personne(est_consciente=False))
    def protocole_hypoglycemie_2(self):
        print("****Oxygenotherapie pour un objectif de SpO2>94% Mise en place d'une voie veineuse peripherique Resucrage per voie intraveineuse a laide d une SOLUTION GLUCOSEE Surveillance continue de la frequance cardiaque puis monitorage cardiaque des que possible ECG recommande apres normalisation de la glycemie")
        self.chaine += "****Oxygenotherapie pour un objectif de SpO2>94% Mise en place d'une voie veineuse peripherique Resucrage per voie intraveineuse a laide d une SOLUTION GLUCOSEE Surveillance continue de la frequance cardiaque puis monitorage cardiaque des que possible ECG recommande apres normalisation de la glycemie \n"


def execution(age, glycemie, conscient):
    engine = Inference()
    engine.reset()
    engine.declare(Personne(age=age,
                            glycemie=glycemie,
                            est_consciente=conscient,
                            ))
    engine.run()

    return engine.chaine