import random
from keywords import CYCLING_ENCOURAGEMENT


def cycling_encouragement(ai):
    ai.text_to_speech(random.choice(CYCLING_ENCOURAGEMENT))
