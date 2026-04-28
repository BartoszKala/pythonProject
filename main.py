import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://www.ing.pl"

GDPR_CONSENT_WITH_ANALYTICS = {3, 7}


def _accept_cookies_with_analytics(page: Page) -> None:
    dostosuj = page.get_by_role("button", name="Dostosuj")
    expect(dostosuj).to_be_visible(timeout=15_000)
    dostosuj.click()

    page.locator(
        "div:nth-child(2) > .cookie-policy-switch > .cookie-policy-toggle-button"
        " > .cookie-policy-toggle-slider > .cookie-policy-slider-thumb"
    ).click()

    page.get_by_role("button", name="Zaakceptuj zaznaczone").click()
    page.wait_for_load_state("networkidle", timeout=15_000)


def _get_cookie(page: Page, name: str) -> dict | None:
    return next((c for c in page.context.cookies() if c["name"] == name), None)



@pytest.fixture(autouse=True)
def clear_storage(page: Page):
    page.context.clear_cookies()
    yield
    page.context.clear_cookies()



class TestIngCookieConsent:

    def test_cookie_banner_appears(self, page: Page):
        page.goto(BASE_URL, wait_until="domcontentloaded")
        expect(page.get_by_role("button", name="Dostosuj")).to_be_visible(timeout=15_000)

    def test_analytics_cookie_set_after_consent(self, page: Page):
        page.goto(BASE_URL, wait_until="domcontentloaded")
        _accept_cookies_with_analytics(page)

        gdpr = _get_cookie(page, "cookiePolicyGDPR")
        assert gdpr is not None, "Brak ciastka cookiePolicyGDPR po wyrażeniu zgody"

        value = int(gdpr["value"])
        assert value in GDPR_CONSENT_WITH_ANALYTICS, (
            f"cookiePolicyGDPR={value} nie wskazuje na zgodę analityczną "
            f"(oczekiwano jednej z wartości: {GDPR_CONSENT_WITH_ANALYTICS})"
        )

    def test_no_consent_cookies_without_interaction(self, page: Page):
        page.goto(BASE_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(3_000)

        names = [c["name"] for c in page.context.cookies()]

        strict_marketing = ["_fbp", "_gcl_au"]
        found_marketing = [n for n in names if n in strict_marketing]

        assert not found_marketing, (
            f"Wykryto ciastka marketingowe bez zgody: {found_marketing}"
        )