import re
from urllib.parse import urlparse


def extract_url_features(url):

    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed_url = urlparse(url)

    domain = parsed_url.netloc
    domain_without_port = domain.split(":")[0]

    features = {}

    features["URLLength"] = len(url)
    features["DomainLength"] = len(domain_without_port)

    ip_pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"
    features["IsDomainIP"] = int(
        bool(re.match(ip_pattern, domain_without_port))
    )

    domain_parts = domain_without_port.split(".")

    if len(domain_parts) > 2:
        features["NoOfSubDomain"] = len(domain_parts) - 2
    else:
        features["NoOfSubDomain"] = 0

    number_of_letters = sum(
        character.isalpha() for character in url
    )

    features["NoOfLettersInURL"] = number_of_letters

    number_of_digits = sum(
        character.isdigit() for character in url
    )

    features["NoOfDegitsInURL"] = number_of_digits

    if len(url) > 0:
        features["LetterRatioInURL"] = number_of_letters / len(url)
    else:
        features["LetterRatioInURL"] = 0

    if len(url) > 0:
        features["DegitRatioInURL"] = number_of_digits / len(url)
    else:
        features["DegitRatioInURL"] = 0

    features["NoOfEqualsInURL"] = url.count("=")
    features["NoOfQMarkInURL"] = url.count("?")
    features["NoOfAmpersandInURL"] = url.count("&")

    special_characters = sum(
        not character.isalnum()
        for character in url
        if character not in "://."
    )

    features["NoOfOtherSpecialCharsInURL"] = special_characters

    if len(url) > 0:
        features["SpacialCharRatioInURL"] = special_characters / len(url)
    else:
        features["SpacialCharRatioInURL"] = 0

    features["IsHTTPS"] = int(
        parsed_url.scheme.lower() == "https"
    )

    return features
if __name__ == "__main__":
    test_url = "https://www.google.com"

    features = extract_url_features(test_url)

    print("Extracted URL features:")

    for name, value in features.items():
        print(name, "=", value)