import html
import os

from brevo import Brevo
from brevo.transactional_emails import (
    SendTransacEmailRequestSender,
    SendTransacEmailRequestToItem,
)


def send_enquiry_email(enquiry):
    """
    Send a new customer enquiry to the manager
    using Brevo transactional email.
    """

    api_key = os.getenv("BREVO_API_KEY")
    sender_email = os.getenv("BREVO_SENDER_EMAIL")
    sender_name = os.getenv(
        "BREVO_SENDER_NAME",
        "Anmol Automobiles",
    )
    manager_email = os.getenv("MANAGER_EMAIL")

    if not api_key:
        raise ValueError(
            "BREVO_API_KEY is not configured."
        )

    if not sender_email:
        raise ValueError(
            "BREVO_SENDER_EMAIL is not configured."
        )

    if not manager_email:
        raise ValueError(
            "MANAGER_EMAIL is not configured."
        )

    # ------------------------------------------------------
    # Escape user-provided values before putting them
    # into HTML email.
    # ------------------------------------------------------

    customer_name = html.escape(
        enquiry.customer_name
    )

    phone = html.escape(
        enquiry.phone
    )

    vehicle = html.escape(
        enquiry.vehicle or "General Enquiry"
    )

    message = html.escape(
        enquiry.message
    )

    created_at = enquiry.created_at.strftime(
        "%d %B %Y, %I:%M %p"
    )

    # ------------------------------------------------------
    # EMAIL HTML
    # ------------------------------------------------------

    email_content = f"""
    <html>
      <body style="
        margin: 0;
        padding: 0;
        background-color: #f8faf9;
        font-family: Arial, sans-serif;
        color: #1f2937;
      ">

        <div style="
          max-width: 650px;
          margin: 0 auto;
          padding: 30px 20px;
        ">

          <div style="
            background: #ffffff;
            border-radius: 16px;
            padding: 30px;
            border: 1px solid #e5e7eb;
          ">

            <h2 style="
              margin-top: 0;
              color: #123c35;
            ">
              New Customer Enquiry
            </h2>

            <p style="
              color: #6b7280;
              margin-bottom: 25px;
            ">
              A new enquiry has been submitted
              through the Anmol Automobiles website.
            </p>

            <div style="
              background: #f8faf9;
              border-radius: 12px;
              padding: 20px;
            ">

              <p>
                <strong>Customer:</strong>
                {customer_name}
              </p>

              <p>
                <strong>Phone:</strong>
                <a
                  href="tel:{phone}"
                  style="color: #0f5c4d;"
                >
                  {phone}
                </a>
              </p>

              <p>
                <strong>Vehicle:</strong>
                {vehicle}
              </p>

              <p>
                <strong>Message:</strong>
              </p>

              <div style="
                background: #ffffff;
                border-radius: 8px;
                padding: 15px;
                line-height: 1.6;
                border: 1px solid #e5e7eb;
              ">
                {message}
              </div>

              <p>
                <strong>Status:</strong>
                NEW
              </p>

              <p>
                <strong>Submitted:</strong>
                {created_at}
              </p>

            </div>

            <p style="
              margin-top: 25px;
              margin-bottom: 0;
              color: #9ca3af;
              font-size: 13px;
            ">
              Anmol Automobiles
            </p>

          </div>

        </div>

      </body>
    </html>
    """

    # ------------------------------------------------------
    # BREVO CLIENT
    # ------------------------------------------------------

    client = Brevo(
        api_key=api_key
    )

    # ------------------------------------------------------
    # SEND EMAIL
    # ------------------------------------------------------

    result = (
        client.transactional_emails.send_transac_email(
            subject=(
                "New Customer Enquiry - "
                "Anmol Automobiles"
            ),

            html_content=email_content,

            sender=(
                SendTransacEmailRequestSender(
                    name=sender_name,
                    email=sender_email,
                )
            ),

            to=[
                SendTransacEmailRequestToItem(
                    name="Manager",
                    email=manager_email,
                )
            ],
        )
    )

    return result