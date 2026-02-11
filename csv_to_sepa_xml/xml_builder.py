"""
SEPA XML generation from payment data.
"""

import logging
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

logger = logging.getLogger(__name__)


def build_sepa_xml(payments, company_name=None, company_iban=None, company_bic=None):
    """
    Convert a list of payments into SEPA XML format.

    Arguments:
        payments: List of payment dictionaries from read_csv_file()
        company_name: Override for debtor name
        company_iban: Override for debtor IBAN
        company_bic: Override for debtor BIC

    Returns:
        A string containing the complete XML
    """
    from .config import DEFAULT_COMPANY_NAME, DEFAULT_COMPANY_IBAN, DEFAULT_COMPANY_BIC
    
    # Use provided values or fall back to defaults
    name = company_name or DEFAULT_COMPANY_NAME
    iban = company_iban or DEFAULT_COMPANY_IBAN
    bic = company_bic or DEFAULT_COMPANY_BIC

    # The namespace tells banks which XML standard we're using
    namespace = "urn:iso:std:iso:20022:tech:xsd:pain.001.001.03"

    # Create the root element (the top of our tree)
    root = ET.Element("Document", xmlns=namespace)

    # Create the main container
    main = ET.SubElement(root, "CstmrCdtTrfInitn")

    # --- GROUP HEADER ---
    header = ET.SubElement(main, "GrpHdr")
    message_id = "MSG" + datetime.now().strftime("%Y%m%d%H%M%S")
    ET.SubElement(header, "MsgId").text = message_id
    ET.SubElement(header, "CreDtTm").text = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    ET.SubElement(header, "NbOfTxs").text = str(len(payments))

    total = sum(float(p.get('amount', 0)) for p in payments)
    ET.SubElement(header, "CtrlSum").text = f"{total:.2f}"

    initiator = ET.SubElement(header, "InitgPty")
    ET.SubElement(initiator, "Nm").text = name

    # --- PAYMENT INFORMATION ---
    payment_info = ET.SubElement(main, "PmtInf")
    payment_id = "PMT" + datetime.now().strftime("%Y%m%d%H%M%S")
    ET.SubElement(payment_info, "PmtInfId").text = payment_id
    ET.SubElement(payment_info, "PmtMtd").text = "TRF"
    ET.SubElement(payment_info, "NbOfTxs").text = str(len(payments))
    ET.SubElement(payment_info, "CtrlSum").text = f"{total:.2f}"

    payment_type = ET.SubElement(payment_info, "PmtTpInf")
    service_level = ET.SubElement(payment_type, "SvcLvl")
    ET.SubElement(service_level, "Cd").text = "SEPA"

    ET.SubElement(payment_info, "ReqdExctnDt").text = datetime.now().strftime("%Y-%m-%d")

    # --- DEBTOR (YOUR COMPANY) ---
    debtor = ET.SubElement(payment_info, "Dbtr")
    ET.SubElement(debtor, "Nm").text = name

    debtor_account = ET.SubElement(payment_info, "DbtrAcct")
    debtor_account_id = ET.SubElement(debtor_account, "Id")
    ET.SubElement(debtor_account_id, "IBAN").text = iban

    debtor_bank = ET.SubElement(payment_info, "DbtrAgt")
    bank_id = ET.SubElement(debtor_bank, "FinInstnId")
    ET.SubElement(bank_id, "BIC").text = bic

    ET.SubElement(payment_info, "ChrgBr").text = "SLEV"

    # --- INDIVIDUAL PAYMENTS ---
    for i, payment in enumerate(payments, start=1):
        transaction = ET.SubElement(payment_info, "CdtTrfTxInf")

        pmt_id = ET.SubElement(transaction, "PmtId")
        end_to_end_id = f"E2E{datetime.now().strftime('%Y%m%d')}{i:04d}"
        ET.SubElement(pmt_id, "EndToEndId").text = end_to_end_id

        amount_element = ET.SubElement(transaction, "Amt")
        instructed_amount = ET.SubElement(amount_element, "InstdAmt", Ccy="EUR")
        instructed_amount.text = f"{float(payment.get('amount', 0)):.2f}"

        if payment.get('bic'):
            creditor_bank = ET.SubElement(transaction, "CdtrAgt")
            creditor_bank_id = ET.SubElement(creditor_bank, "FinInstnId")
            ET.SubElement(creditor_bank_id, "BIC").text = payment.get('bic', '')

        creditor = ET.SubElement(transaction, "Cdtr")
        ET.SubElement(creditor, "Nm").text = payment.get('name', '')

        creditor_account = ET.SubElement(transaction, "CdtrAcct")
        creditor_account_id = ET.SubElement(creditor_account, "Id")
        ET.SubElement(creditor_account_id, "IBAN").text = payment.get('iban', '')

        if payment.get('reference'):
            remittance = ET.SubElement(transaction, "RmtInf")
            ET.SubElement(remittance, "Ustrd").text = payment.get('reference', '')

    # --- CONVERT TO PRETTY XML STRING ---
    xml_string = ET.tostring(root, encoding='unicode')
    dom = minidom.parseString(xml_string)
    pretty_xml = dom.toprettyxml(indent="  ")

    logger.info(f"Generated XML with {len(payments)} payments, total EUR {total:.2f}")

    return pretty_xml
