import re
from urllib.parse import urlparse


def extract_url_features(url):

    # Add http:// if the URL does not contain a scheme
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed_url = urlparse(url)

    domain = parsed_url.netloc
    domain_without_port = domain.split(":")[0]

    features = {}

    # 1. URL length
    features["URLLength"] = len(url)

    # 2. Domain length
    features["DomainLength"] = len(domain_without_port)

    # 3. Check whether domain is an IP address
    ip_pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"

    features["IsDomainIP"] = int(
        bool(re.match(ip_pattern, domain_without_port))
    )

    # 4. Number of subdomains
    domain_parts = domain_without_port.split(".")

    if len(domain_parts) > 2:
        features["NoOfSubDomain"] = len(domain_parts) - 2
    else:
        features["NoOfSubDomain"] = 0

    # 5. Number of letters
    number_of_letters = sum(
        character.isalpha()
        for character in url
    )

    features["NoOfLettersInURL"] = number_of_letters

    # 6. Number of digits
    number_of_digits = sum(
        character.isdigit()
        for character in url
    )

    features["NoOfDegitsInURL"] = number_of_digits

    # 7. Letter ratio
    if len(url) > 0:
        features["LetterRatioInURL"] = (
            number_of_letters / len(url)
        )
    else:
        features["LetterRatioInURL"] = 0

    # 8. Digit ratio
    if len(url) > 0:
        features["DegitRatioInURL"] = (
            number_of_digits / len(url)
        )
    else:
        features["DegitRatioInURL"] = 0

    # 9. Number of =
    features["NoOfEqualsInURL"] = url.count("=")

    # 10. Number of ?
    features["NoOfQMarkInURL"] = url.count("?")

    # 11. Number of &
    features["NoOfAmpersandInURL"] = url.count("&")

    # 12. Other special characters
    special_characters = sum(
        not character.isalnum()
        for character in url
        if character not in "://."
    )

    features["NoOfOtherSpecialCharsInURL"] = special_characters

    # 13. Special character ratio
    if len(url) > 0:
        features["SpacialCharRatioInURL"] = (
            special_characters / len(url)
        )
    else:
        features["SpacialCharRatioInURL"] = 0

    # 14. HTTPS
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