import os
import requests
from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """
    Scrape information from LinkedIn profiles,
    Manually scrape the infor mation from the LinkedIn profile
    """

    if mock:
        # For testing purposes, we will use a static json file
        linkedin_profile_url = "https://gist.githubusercontent.com/jspark67/3d8ac22a690c82d6172212a720aec56a/raw/d8efe166d18c688d3c94e6df874a2b7bce4a8f5d/jspark.json"

        response = requests.get(
            linkedin_profile_url,
            timeout=10,
        )
    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization": f'Bearer {os.environ["PROXYCURL_API_KEY"]}'}
        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers=header_dic,
            timeout=10,
        )

    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/junseokpark/",
            mock=True,
        )
    )
