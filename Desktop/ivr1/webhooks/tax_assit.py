from pathlib import Path
from typing import Any, Optional, Tuple

from jaxl.ivr.frontend.base import (
    BaseJaxlIVRWebhook,
    ConfigPathOrDict,
    JaxlIVRRequest,
    JaxlIVRResponse,
)


class JaxlIVRTaxInformationWebhook(BaseJaxlIVRWebhook):
    """tax_assit.json webhook implementation."""

    @staticmethod
    def config() -> ConfigPathOrDict:
        return Path(__file__).parent.parent / "schemas" / "tax_information.json"

    def setup(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        return JaxlIVRResponse(
            message="Welcome to the Tax Information and Assistance. Please select from the following options to proceed further",
            options=[(item["option"], item["description"]) for item in request.config["ivr"]["main_menu"]]
        )

    def teardown(self, request: JaxlIVRRequest) -> None:
       
        pass

    def handle_option(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        selected_option = request.dtmf
        main_menu = request.config["ivr"]["main_menu"]

        for item in main_menu:
            if item["option"] == selected_option:
                if "sub_menu" in item:
                    return JaxlIVRResponse(
                        message=f"You selected {item['description']}.",
                        options=[(sub_item["option"], sub_item["description"]) for sub_item in item["sub_menu"]]
                    )
                elif "instructions" in item:
                    return JaxlIVRResponse(
                        message=" ".join(item["instructions"]),
                        options=[("4", "Go back to the main menu.")]
                    )
                elif selected_option == "0":
                    return JaxlIVRResponse(
                        message="Please hold while we connect you to a tax assistance representative."
                    )
                elif selected_option == "5":
                    return self.setup(request)

        return JaxlIVRResponse(
            message="Invalid option selected. Please try again.",
            options=[(item["option"], item["description"]) for item in main_menu]
        )

    def stream(
        self,
        request: JaxlIVRRequest,
        chunk_id: int,
        sstate: Any,
    ) -> Optional[Tuple[Any, JaxlIVRResponse]]:
        raise NotImplementedError()