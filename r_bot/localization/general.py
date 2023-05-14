from discord import OptionChoice

oc_yes = {
    "en-GB": "Yes",
    "uk": "Так",
    # "ru": "Да",
}

oc_no = {
    "en-GB": "No",
    "uk": "Ні",
    # "ru": "Да",
}

option_choice_yes = OptionChoice(name=oc_yes['en-GB'], name_localizations=oc_yes, value=1)
option_choice_no = OptionChoice(name=oc_no['en-GB'], name_localizations=oc_no, value=0)