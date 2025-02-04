from fastapi import APIRouter, FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Invoice(BaseModel):
    id: str
    title: str | None = None
    customer: str
    total: float


class InvoiceEvent(BaseModel):
    description: str
    paid: bool


class InvoiceEventReceived(BaseModel):
    ok: bool


invoices_callback_url = APIRouter()


@invoices_callback_url.post(
    "{$callback_url}/invoices/{$request.body.id}", response_model=InvoiceEventReceived
)
def invoice_notification(body: InvoiceEvent):
    pass

# ------------------ INVOICE Callback --------------------------------
@app.post("/invoices/callback/")
def invoices_callback(body: InvoiceEvent):
    return {
        "ok": True,
    }

# -------------------- CREATE Invoice ---------------------------------
@app.post("/invoices/", callbacks=invoices_callback_url.routes)
def create_invoice(invoice: Invoice, callback_url: HttpUrl | None = None):
    """
    Create an invoice.

    This will (let's imagine) let the API user (some external developer) create an
    invoice.

    And this path operation will:

    * Send the invoice to the client.
    * Collect the money from the client.
    * Send a notification back to the API user (the external developer), as a callback.
        * At this point is that the API will somehow send a POST request to the
            external API with the notification of the invoice event
            (e.g. "payment successful").
    """
    # Send the invoice, collect the money, send the notification (the callback)
    return {"msg": "Invoice received"}
