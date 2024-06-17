APP = 'APP'

# Status types
STATUS_TYPE = {
    APP: "App",
    "CP": "CustomerPortal",
    "SMS": "Sms",
    "EMAIL": "Email",
    "PAYMENT": "Payment",
    "TEBT": "TEBT",
    "IOC": "IOC",
    "QUOTE": "Quote",
    "SVG": "SVG",
    "LEAD_FORM": "LeadFrom"
}

# Non retryable exception codes
BAD_REQUEST = 'BAD_REQUEST'
GENERIC_FAILURE = 'GENERIC_FAILURE'

NONRETRYABLE_CODE = {
    BAD_REQUEST: "BadRequest",  # Generic exception which can be used for bad request
    GENERIC_FAILURE: "GenericFailure",  # HDFC Customer portal API failed
    "PAYU_HASH_MISMATCH": "PayuHashMismatch",
    "PAYZAPP_PICKUP_FAIL": "PazyappPickupFail"
}

# Exception fields
EXCEPTION_TYPE_NON_RETRYABLE = "NonRetryable"
EXCEPTION_TYPE_RETRYABLE = "Retryable"

# Retryable exception codes
RETRYABLE_CODE = {
    "API_UNREACHABLE": "ApiUnreachable",  # any generic tpt API is unreachable for moment
    "SMS_FAILURE": "SmsApiFailure",
    "EMAIL_FAILURE": "EmailApiFailure"
}