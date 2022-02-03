import argparse
import io
import json
import os
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from typing import Dict, Iterable, Optional

import pytest
import regex
import tweepy
from tweepy.models import Media, Status
from tweepy.errors import TweepyException


# Add your twitter info here:
api_key = ""
api_secret = ""
access_token = ""
access_token_secret = ""


URL_REGEX = regex.compile(
    r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:1|247|3dom|abogado|ac|academy|accountant|accountants|actor|adult|agency|ai|airforce|am|apartments|api|app|archi|army|art|articles|asia|associates|attorney|auction|audio|auto|autos|baby|band|bar|bargains|basketball|bayern|beauty|beer|best|bible|bid|bike|bingo|bio|biz|black|blackfriday|blog|blue|boats|bond|boston|boutique|broker|build|builders|business|buzz|c|cab|cafe|cam|camera|camp|capital|car|cards|care|careers|cars|casa|cash|casino|catering|cc|center|ceo|cfd|charity|chat|cheap|christmas|church|city|claims|cleaning|click|clinic|clothing|cloud|club|co|coach|codes|coffee|college|com|community|company|compare|computer|condos|construction|consulting|contact|contractors|cooking|cool|country|coupons|courses|credit|creditcard|cricket|cruises|cx|cymru|cyou|dance|date|dating|day|dealer|deals|defi|degen|degree|delivery|democrat|dental|dentist|desi|design|dev|diamonds|diet|digital|direct|directory|discount|doctor|dog|domains|dookie|download|earth|eco|education|email|energy|engineer|engineering|enterprises|equipment|estate|eu|events|exchange|expert|exposed|express|fail|faith|fam|family|fan|fans|farm|fashion|feedback|finance|financial|fish|fishing|fit|fitness|flights|florist|flowers|fm|fo|football|forex|forsale|forum|foundation|fun|fund|furniture|futbol|fyi|gallery|game|games|garden|gay|gift|gifts|gives|glass|global|gmbh|gold|golf|graphics|gratis|green|gripe|group|guide|guitars|guru|hair|haus|health|healthcare|help|hiphop|hiv|hockey|holdings|holiday|homes|horse|hospital|host|hosting|house|how|icu|id|immo|immobilien|in|inc|industries|info|ink|institute|insure|international|investments|io|irish|ism|ize|jetzt|jewelry|jobs|js|juegos|kaufen|kim|kitchen|kyoto|la|land|law|lawyer|lease|legal|lgbt|life|lighting|limited|limo|link|live|llc|loan|loans|lol|london|lotto|love|ltd|ltda|luxe|luxury|maison|makeup|management|market|marketing|markets|mba|me|media|melbourne|memorial|men|menu|miami|mobi|moda|moe|mom|money|monster|mortgage|motorcycles|movie|nagoya|name|navy|net|network|new|news|ninja|nrw|nyc|observer|one|online|onlinenews|ooo|org|organic|osaka|owbo|page|pal|partners|parts|party|pet|photo|photography|photos|pics|pictures|pink|pizza|place|plumbing|plus|poker|porn|press|pro|productions|promo|properties|property|protection|pub|pw|qpon|quest|racing|realty|recipes|red|rehab|reise|reisen|rent|rentals|repair|report|republican|rest|restaurant|review|reviews|rip|rocks|rodeo|rugby|run|saarland|sale|salon|sarl|sats|sbs|school|schule|science|security|select|services|sex|sexy|sh|shiksha|shoes|shop|shopping|show|singles|site|ski|skin|soccer|social|software|solar|solutions|soy|spa|space|srl|startup|storage|store|stream|studio|study|style|sucks|supplies|supply|support|surf|surgery|sydney|systems|tattoo|tax|taxi|team|tech|technology|tel|tennis|theater|theatre|tickets|tienda|tips|tires|today|tokyo|tools|top|tours|town|toys|trade|trading|training|travel|tube|tv|tx|txt|uk|university|uno|us|use|vacations|vegas|ventures|vet|viajes|video|villas|vin|vip|vision|visit|vodka|vote|voto|voyage|vrmmo|wales|wang|watch|webcam|website|wedding|wiki|win|wine|work|works|world|wtf|xn--5tzm5g|xn--6frz82g|xn--czrs0t|xn--fjq720a|xn--q9jyb4c|xn--unup4y|xn--vhquv|xr|xxx|xyz|yachts|yo|yoga|yokohama|yzx|zen|zone|edu|gov|mil|aero|cat|coop|int|museum|post|ad|ae|af|ag|al|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cd|cf|cg|ch|ci|ck|cl|cm|cn|cr|cs|cu|cv|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|fi|fj|fk|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|ie|il|im|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tw|tz|ua|ug|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:1|247|3dom|abogado|ac|academy|accountant|accountants|actor|adult|agency|ai|airforce|am|apartments|api|app|archi|army|art|articles|asia|associates|attorney|auction|audio|auto|autos|baby|band|bar|bargains|basketball|bayern|beauty|beer|best|bible|bid|bike|bingo|bio|biz|black|blackfriday|blog|blue|boats|bond|boston|boutique|broker|build|builders|business|buzz|c|cab|cafe|cam|camera|camp|capital|car|cards|care|careers|cars|casa|cash|casino|catering|cc|center|ceo|cfd|charity|chat|cheap|christmas|church|city|claims|cleaning|click|clinic|clothing|cloud|club|co|coach|codes|coffee|college|com|community|company|compare|computer|condos|construction|consulting|contact|contractors|cooking|cool|country|coupons|courses|credit|creditcard|cricket|cruises|cx|cymru|cyou|dance|date|dating|day|dealer|deals|defi|degen|degree|delivery|democrat|dental|dentist|desi|design|dev|diamonds|diet|digital|direct|directory|discount|doctor|dog|domains|dookie|download|earth|eco|education|email|energy|engineer|engineering|enterprises|equipment|estate|eu|events|exchange|expert|exposed|express|fail|faith|fam|family|fan|fans|farm|fashion|feedback|finance|financial|fish|fishing|fit|fitness|flights|florist|flowers|fm|fo|football|forex|forsale|forum|foundation|fun|fund|furniture|futbol|fyi|gallery|game|games|garden|gay|gift|gifts|gives|glass|global|gmbh|gold|golf|graphics|gratis|green|gripe|group|guide|guitars|guru|hair|haus|health|healthcare|help|hiphop|hiv|hockey|holdings|holiday|homes|horse|hospital|host|hosting|house|how|icu|id|immo|immobilien|in|inc|industries|info|ink|institute|insure|international|investments|io|irish|ism|ize|jetzt|jewelry|jobs|js|juegos|kaufen|kim|kitchen|kyoto|la|land|law|lawyer|lease|legal|lgbt|life|lighting|limited|limo|link|live|llc|loan|loans|lol|london|lotto|love|ltd|ltda|luxe|luxury|maison|makeup|management|market|marketing|markets|mba|me|media|melbourne|memorial|men|menu|miami|mobi|moda|moe|mom|money|monster|mortgage|motorcycles|movie|nagoya|name|navy|net|network|new|news|ninja|nrw|nyc|observer|one|online|onlinenews|ooo|org|organic|osaka|owbo|page|pal|partners|parts|party|pet|photo|photography|photos|pics|pictures|pink|pizza|place|plumbing|plus|poker|porn|press|pro|productions|promo|properties|property|protection|pub|pw|qpon|quest|racing|realty|recipes|red|rehab|reise|reisen|rent|rentals|repair|report|republican|rest|restaurant|review|reviews|rip|rocks|rodeo|rugby|run|saarland|sale|salon|sarl|sats|sbs|school|schule|science|security|select|services|sex|sexy|sh|shiksha|shoes|shop|shopping|show|singles|site|ski|skin|soccer|social|software|solar|solutions|soy|spa|space|srl|startup|storage|store|stream|studio|study|style|sucks|supplies|supply|support|surf|surgery|sydney|systems|tattoo|tax|taxi|team|tech|technology|tel|tennis|theater|theatre|tickets|tienda|tips|tires|today|tokyo|tools|top|tours|town|toys|trade|trading|training|travel|tube|tv|tx|txt|uk|university|uno|us|use|vacations|vegas|ventures|vet|viajes|video|villas|vin|vip|vision|visit|vodka|vote|voto|voyage|vrmmo|wales|wang|watch|webcam|website|wedding|wiki|win|wine|work|works|world|wtf|xn--5tzm5g|xn--6frz82g|xn--czrs0t|xn--fjq720a|xn--q9jyb4c|xn--unup4y|xn--vhquv|xr|xxx|xyz|yachts|yo|yoga|yokohama|yzx|zen|zone|edu|gov|mil|aero|cat|coop|int|museum|post|ad|ae|af|ag|al|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cd|cf|cg|ch|ci|ck|cl|cm|cn|cr|cs|cu|cv|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|fi|fj|fk|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|ie|il|im|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tw|tz|ua|ug|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
)

# Mapping from the name that will be used in a code block, to what carbon wants
CODE_BLOCK_LANGUAGE_MAP = {
    "py": "python",
    "js": "javascript",
    "c": "text/x-csrc",
    "cpp": "text/x-c++src",
    "sh": "application/x-sh",
    "bash": "application/x-sh",
    "text": "text",
    "plaintext": "text",
}


class CodeImageCreationError(Exception):
    ...


def tweet_length(tweet: str) -> int:
    """Returns how long twitter thinks this tweet will be."""
    # Since twitter treats every link as 23 characters,
    # we just replace every URL with any 23 characters.
    tweet = URL_REGEX.sub("some-23-characters-here", tweet)

    char_count = 0
    # '\X' matches each grapheme (visible character), that way
    # even complex emojis and other characters are counted as 1 char
    for char in regex.findall(r"\X", tweet):
        if char.isascii():
            char_count += 1
        else:
            # Assuming all non ascii characters like emojis to be 2 chars
            char_count += 2

    return char_count


def twitter_login() -> tweepy.API:
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    try:
        api.verify_credentials()
    except TweepyException:
        print("Unable to authorize user. Probably bad credentials.")
        raise

    return api


def upload_image(api: tweepy.API, image_data: bytes) -> Media:
    image_file = io.BytesIO(image_data)
    return api.media_upload("code.png", file=image_file)


def tweet(api: tweepy.API, text: str, media_ids: Iterable[Media] = ()) -> None:
    """Login to your account and send a tweet."""
    try:
        api.update_status(text, media_ids=media_ids)
    except TweepyException as exc:
        print("Unable to send tweet. Probably credentials don't have write access.")
        print("Error:", *exc.args)
        return


def tweet_thread(
    api: tweepy.API, tweets: Iterable[str], media_ids: Iterable[Iterable[Media]] = ()
) -> Optional[Status]:
    """Tweet out a thread (a sequence of tweets)."""

    last_tweet = None
    for idx, (tweet, medias) in enumerate(zip(tweets, media_ids)):
        try:
            last_tweet = api.update_status(
                tweet,
                in_reply_to_status_id=getattr(last_tweet, "id", None),
                auto_populate_reply_metadata=True,
                media_ids=medias,
            )
        except TweepyException as exc:
            print(f"Unable to send tweet {idx}.")
            print("Error:", *exc.args)
            return last_tweet
    return last_tweet


def create_code_image(
    code: str,
    language: str,
    config: Optional[Dict[str, str]] = None,
) -> bytes:
    req = Request("https://carbonara-42.herokuapp.com/api/cook")
    req.add_header("Content-Type", "application/json")

    if config is None:
        config = {}

    config["code"] = code
    config["language"] = CODE_BLOCK_LANGUAGE_MAP[language]

    try:
        with urlopen(req, data=json.dumps(config).encode()) as response:
            image = response.read()

    except HTTPError as exc:
        response_body = exc.fp.read().decode()
        raise CodeImageCreationError(response_body) from None

    return image


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file")
    parser.add_argument("--config")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"File {args.file} does not exist!")
        return 1

    with open(args.file) as f:
        code = f.read()

    if args.config:
        if not os.path.exists(args.config):
            print(f"Config file {args.config} does not exist!")
            return 1

        with open(args.config) as f:
            config = json.load(f)
    else:
        config = None

    try:
        image_data = create_code_image(code, "text", config)
    except CodeImageCreationError as exc:
        print("Error creating code image:", *exc.args)
        return 1

    try:
        api = twitter_login()
        media = upload_image(api, image_data)
        tweet(api, "Test tweet!", (media,))
    except TweepyException as exc:
        print("Error while tweeting:", *exc.args)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

###########################################


@pytest.mark.parametrize(
    ("tweet", "length"),
    (
        ("Hello!", 6),
        ("🐍✨🐍", 6),  # All emojis are considered 2 characters
        ("👨🏽‍💻👨‍👩‍👦‍👦👨🏼‍🤝‍👨🏽", 6),  # Even ones with a lot of joins and modifiers
        ("桜さくら", 8),  # It seems all non ascii characters are also 2 characters
        ("a.cx;a.cx", 47),  # Links are 23 characters, regardless of their actual length
        ("a-really-really-really-long.link a-really-really-really-long.link", 47),
        ("Hi!~https://subdomain.example-domain.cool:8765/abc?def=ghi+jkl&mnop", 27),
    ),
)
def test_tweet_length(tweet: str, length: int) -> None:
    assert tweet_length(tweet) == length
