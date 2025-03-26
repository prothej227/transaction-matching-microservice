from pydantic import BaseModel, Field
from datetime import date

class ARRecord(BaseModel):
    """ Open AR Entity """
    erpDocumentNumber: str = Field(..., alias="erpDocumentNumber")
    documentDate: date = Field(..., alias="documentDate")
    customerNumber: str = Field(..., alias="customerNumber")
    customerName: str = Field(..., alias="customerName")
    paymentTerms: str
    dueDate: date = Field(..., alias="dueDate")
    invoiceAmount: float
    balanceAmount: float
    debitCreditIndicator: str = Field(..., alias="debitCreditIndicator")
    companyCode: str = Field(..., alias="companyCode")


class BankStatementRecord(BaseModel):
    """ Bank Statement Entity """
    id: int = Field(..., description="References to the actual Bank Satement PK")
    transactionDate: str
    amount: float
    reference: str
    longText: str
