"""
Ingest real production-like data into local OpenSearch matching the actual structure.
Uses separate indices for documents, comments, and comments_extracted_text.
"""

from opensearchpy import OpenSearch


def ingest_opensearch():
    """Insert real production-like documents, comments, and extracted text into local OpenSearch"""
    
    client = OpenSearch(
        hosts=[{"host": "localhost", "port": 9200}],
        use_ssl=False,
        verify_certs=False,
    )
    
    # Delete and recreate documents index
    if client.indices.exists(index="documents_text"):
        client.indices.delete(index="documents_text")
    
    # Create with proper mapping
    client.indices.create(
        index="documents_text",
        body={
            "mappings": {
                "properties": {
                    "docketId": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
                    },
                    "documentId": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
                    },
                    "documentText": {
                        "type": "text"
                    }
                }
            }
        }
    )
    
    # Delete and recreate comments index
    if client.indices.exists(index="comments"):
        client.indices.delete(index="comments")
    
    client.indices.create(
        index="comments",
        body={
            "mappings": {
                "properties": {
                    "commentId": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
                    },
                    "commentText": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
                    },
                    "docketId": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
                    }
                }
            }
        }
    )
    
    # Delete and recreate comments_extracted_text index
    if client.indices.exists(index="comments_extracted_text"):
        client.indices.delete(index="comments_extracted_text")
    
    client.indices.create(
        index="comments_extracted_text",
        body={
            "mappings": {
                "properties": {
                    "attachmentId": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
                    },
                    "commentId": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
                    },
                    "docketId": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
                    },
                    "extractedMethod": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
                    },
                    "extractedText": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
                    }
                }
            }
        }
    )
    
    # Insert documents
    documents = [
        {
            "docketId": "CMS-2025-0001",
            "documentId": "CMS-2025-0001-0001",
            "document_text": "[Federal Register Volume 90, Number 2 (Friday, January 3, 2025)] [Notices] [Pages 321-322] From the Federal Register Online via the Government Publishing Office [www.gpo.gov] [FR Doc No: 2024-31567] ----------------------------------------------------------------------- DEPARTMENT OF HEALTH AND HUMAN SERVICES Centers for Medicare & Medicaid Services [Document Identifiers: CMS-10565 and CMS-1763] Agency Information Collection Activities: Proposed Collection; Comment Request AGENCY: Centers for Medicare & Medicaid Services, Health and Human Services (HHS). ACTION: Notice. ----------------------------------------------------------------------- SUMMARY: The Centers for Medicare & Medicaid Services (CMS) is announcing an opportunity for the public to comment on CMS' intention to collect information from the public. Under the Paperwork Reduction Act of 1995 (PRA), Federal agencies are required to publish notice in the Federal Register concerning each proposed collection of information (including each proposed extension or reinstatement of an existing collection of information) and to allow 60 days for public comment on the proposed action. Interested persons are invited to send comments regarding our burden estimates or any other aspect of this collection of information, including the necessity and utility of the proposed information collection for the proper performance of the agency's functions, the accuracy of the estimated burden, ways to enhance the quality, utility, and clarity of the information to be collected, and the use of automated collection techniques or other forms of information technology to minimize the information collection burden. DATES: Comments must be received by March 4, 2025. ADDRESSES: When commenting, please reference the document identifier or OMB control number. To be assured consideration, comments and recommendations must be submitted in any one of the following ways: 1. Electronically. You may send your comments electronically to http://www.regulations.gov. Follow the instructions for ``Comment or Submission'' or ``More Search Options'' to find the information collection document(s) that are accepting comments. 2. By regular mail. You may mail written comments to the following address: CMS, Office of Strategic Operations and Regulatory Affairs, Division of Regulations Development, Attention: Document Identifier/OMB Control Number: __, Room C4-26-05, 7500 Security Boulevard, Baltimore, Maryland 21244-1850. To obtain copies of a supporting statement and any related forms for the proposed collection(s) summarized in this notice, please access the CMS PRA website by copying and pasting the following web address into your web browser: https://www.cms.gov/Regulations-and-Guidance/Legislation/PaperworkReductionActof1995/PRA-Listing. FOR FURTHER INFORMATION CONTACT: William N. Parham at (410) 786-4669. SUPPLEMENTARY INFORMATION: Contents This notice sets out a summary of the use and burden associated with the following information collections. More detailed information can be found in each collection's supporting statement and associated materials (see ADDRESSES). CMS-10565 Medicare Advantage Model of Care Submission Requirements CMS-1763 Request for Termination of Medicare Premium Part A, Part B, or Part B Immunosuppressive Drug Coverage (Part B-ID) and Supporting Statute and Regulations Under the PRA (44 U.S.C. 3501-3520), Federal agencies must obtain approval from the Office of Management and Budget (OMB) for each collection of information they conduct or sponsor. The term ``collection of information'' is defined in 44 U.S.C. 3502(3) and 5 CFR 1320.3(c) and includes agency requests or requirements that members of the public submit reports, keep records, or provide information to a third party. Section 3506(c)(2)(A) of the PRA requires Federal agencies to publish a 60-day notice in the Federal Register concerning each proposed collection of information, including each proposed extension or reinstatement of an existing collection of information, before submitting the collection to OMB for approval. To comply with this requirement, CMS is publishing this notice. Information Collections 1. Type of Information Collection Request: Revision of a currently approved collection; Title of Information Collection: Medicare Advantage Model of Care Submission Requirements; Use: Section 1859(f)(7) of the Act and 42 CFR 422.101(f)(3) requires that all SNP MOCs be approved by NCQA. This approval is based on NCQA's evaluation of SNPs' MOC narratives using MOC scoring guidelines. Section 50311 of the BBA of 2018 modified the MOC requirements for C-SNPs in section 1859 (f)(5)(B)(i-v) of the Act, requiring them to submit on an annual basis. The BBA mandated additional changes for C-SNPs related to care management, HRAs, individualized care plans, a minimum benchmark for scoring, etc., for which CMS has applied these requirements to all SNP types. SNPs will submit initial and renewal MOCs as well as summaries of any substantive off-cycle MOC changes to CMS through HPMS. This is the platform that CMS uses to coordinate communication and the collection of information from MAOs. NCQA and CMS will use information collected in the SNP Application HPMS module to review and approve MOC narratives in order for an MAO to offer a new SNP in the upcoming calendar year(s). This information is used by CMS as part of the MA SNP application process. NCQA and CMS will use information collected in the Renewal Submission section of the HPMS MOC module to review and approve the MOC narrative for the SNP to receive a new approval period and operate in the upcoming calendar year(s). Form Number: CMS-10565 (OMB control number 0938-1296); Frequency: Occasionally; Affected Public: Private Sector, Business or other for-profits; Number of Respondents: 2,088; Total Annual Responses: 2,088; Total Annual Hours: 8,638. (For policy questions regarding this collection contact Daniel Lehman at 410-786-8929.) 2. Type of Information Collection Request: Revision of a currently approved collection; Title of Information Collection: Request for Termination of Medicare Premium Part A, Part B, or Part B Immunosuppressive Drug Coverage (Part B-ID) and Supporting Statute and Regulations; Use: Sections 1818(c)(5), 1818A(c)(2)(B) and 1838(b)(1) of the Act and corresponding regulations at 42 CFR 406.28(a) and 407.27(c) require that a Medicare enrollee wishing to voluntarily terminate Part B or premium Part A coverage file a written request with CMS or SSA. Pursuant to 1838(h) of the Act and the corresponding regulation at 42 CFR 407.62(a), individuals wishing to terminate their Part B-ID coverage must notify SSA. The statute and regulations also specify when coverage ends based upon the date the request for termination is filed. The CMS-1763 is the form used by individuals who wish to terminate their Medicare Part A, Part B or Part B-ID. This 2024 iteration is a revision that does not propose any program changes. Per the Office of Communication's plain language suggestion, the title has been updated to ``Request for Termination of Medicare Premium Part A, Part B, or Part B Immunosuppressive Drug Coverage (Part B-ID).'' The 2024 submission saw an increase in the burden due to utilization of the form and improvement in the accuracy of the data exchanges between CMS and SSA. Updated wage information for a Federal Government employee is also responsible for part of the increase. Form Number: CMS-1763 (OMB control number 0938-0025); Frequency: Biennially; Affected Public: Private Sector--State, Local, or Tribal Governments; and Federal Government; Number of Respondents: 197,518; Total Annual Responses: 197,518; Total Annual Hours: 33,578. (For policy questions regarding this collection contact Tyrissa Woods at 410-786-0286.) William N. Parham, III, Director, Division of Information Collections and Regulatory Impacts, Office of Strategic Operations and Regulatory Affairs. [FR Doc. 2024-31567 Filed 1-2-25; 8:45 am] BILLING CODE 4120-01-P"
        }
    ]
    
    for i, doc in enumerate(documents):
        client.index(index="documents", id=i, body=doc)
    
    # Insert comments
    comments = [
        {
            "commentId": "CMS-2025-0240-0014",
            "commentText": "I am contacting you in my role as the Founder and CEO of Peer Plus Education and Training Advocates, a Chicago-based 501(c)3 that identifies underserved populations in the Midwest area. Peer Plus provides culturally sensitive programs that address the multifaceted issues of people in need of essential health, educational, and psychosocial services.<br/><br/>On behalf of kidney disease patients throughout the Midwest, I ask you to please reconsider the decision to move phosphate lowering treatments (PLT) out of Medicare Part D, which allowed patients to access their treatment from their community pharmacist.",
            "docketId": "CMS-2025-0240"
        },
        {
            "commentId": "CMS-2025-0240-0030",
            "commentText": "Dear Dr. Mehmet Oz,<br/><br/>What if you were told the medication your patient depends on to stay alive is now harder to get &ndash; all because of a decision in Washington D.C.? That&rsquo;s the reality for thousands of kidney patients since Medicare shifted Phosphate Lowering Therapies (PLTs) into a budget-capped payment system on January 1, 2025.",
            "docketId": "CMS-2025-0240"
        },
        {
            "commentId": "CMS-2019-0100-0402",
            "commentText": "Please see the attached document.<br/><br/>Thank you",
            "docketId": "CMS-2019-0100"
        },
        {
            "commentId": "CMS-2019-0100-0415",
            "commentText": "Attached please find comments from BayCare HomeCare in Largo, Florida.",
            "docketId": "CMS-2019-0100"
        },
        {
            "commentId": "CMS-2019-0100-0420",
            "commentText": "The home health agency that I work for is located in Florida and serves approximately 250 unique Medicare beneficiaries each month. Our agency has been subjected to Targeted Probe and Educate, the Value Based Purchasing demonstration project, a multi-year moratorium on new licenses that prevented our agency from achieving organic growth in the geographical footprint that we were able to serve.",
            "docketId": "CMS-2019-0100"
        },
        {
            "commentId": "CMS-2019-0100-0423",
            "commentText": "In addition to my previous comments - Another behavioral assumption related to diagnostic coding is also very concerning to me. In the Conditions of Participation at 484.60(a)(2) requires that all pertinent diagnoses be included in the POC.",
            "docketId": "CMS-2019-0100"
        },
        {
            "commentId": "CMS-2019-0100-0438",
            "commentText": "Dear Administrator Verma: <br/><br/>On behalf of the Academy of Geriatric Physical Therapy of the American Physical Therapy Association (Academy of Geriatric Physical Therapy), I am writing to submit comments in response to the Centers for Medicare and Medicaid Services (CMS) Calendar Year (CY) 2020 Home Health Prospective Payment System (HH PPS) Rate Update.",
            "docketId": "CMS-2019-0100"
        },
        {
            "commentId": "CMS-2019-0100-0424",
            "commentText": "Dear Administrator Verma: <br/><br/>I am writing in response to the request for comments on the Centers for Medicare and Medicaid Services (CMS) Calendar Year (CY) 2020 Home Health Prospective Payment System (PPS) Rate Update proposed rule.<br/>",
            "docketId": "CMS-2019-0100"
        },
        {
            "commentId": "CMS-2019-0100-0431",
            "commentText": "September 8, 2019<br/> <br/>Seema Verma, MPH<br/>Administrator<br/>Centers for Medicare and Medicaid Services<br/>Department of Health and Human Services<br/>Room 445-G<br/>Attn: CMS-1711-P<br/>Hubert Humphrey Building<br/>200 Independence Ave, SW<br/>Washington, DC 20201<br/> <br/>Submitted electronically",
            "docketId": "CMS-2019-0100"
        },
        {
            "commentId": "DEA-2024-0059-16885",
            "commentText": "Official Comment Drug Enforcement Agency ,<br/><br/>I am writing to express my support for the proposal to reclassify marijuana from a Schedule I to a Schedule III substance under the Controlled Substances Act. <br/><br/>This is an important step toward a change in marijuana policy that addresses the decades-long discrimination against Black and Brown communities.",
            "docketId": "DEA-2024-0059"
        }
    ]

    for i, comment in enumerate(comments):
        client.index(index="comments", id=i, body=comment)
    
    # Insert comments_extracted_text
    extracted_texts = [
        {
            "attachmentId": "CMS-2025-0240-0203-1",
            "commentId": "CMS-2025-0240-0203",
            "docketId": "CMS-2025-0240",
            "extractedMethod": "pypdf",
            "extractedText": "FIRM:68395945v1 August 29, 2025 VIA REGULATIONS.GOV FILING Centers for Medicare & Medicaid Services U.S. Department of Health and Human Services Attention: CMS-1830-P P.O. Box 8010 Baltimore, MD 21244-8010 RE: Medicare End-Stage Renal Disease Prospective Payment System for CY 2026"
        },
        {
            "attachmentId": "CMS-2025-0240-0156-1",
            "commentId": "CMS-2025-0240-0156",
            "docketId": "CMS-2025-0240",
            "extractedMethod": "pypdf",
            "extractedText": "1300 17th St. N, Suite 580 • Arlington, VA 22209 • Toll Free Number 1.866.877.4242 www.dialysispatients.org • Email: dpc@dialysispatients.org • Fax 1.888.423.5002 DPC is a 501(c)(4) non-profit organization governed by dialysis patients. Improving Life Through Empowerment August 27, 2025"
        },
        {
            "attachmentId": "CMS-2025-0240-0168-1",
            "commentId": "CMS-2025-0240-0168",
            "docketId": "CMS-2025-0240",
            "extractedMethod": "pypdf",
            "extractedText": "August 18, 2025 Mehmet Oz, MD, MBA Administrator Centers for Medicare & Medicaid Services Department of Health and Human Services 200 Independence Avenue, SW Washington, DC 20201 Re: CMS–1830-P — Medicare Program; End-Stage Renal Disease Prospective Payment System"
        },
        {
            "attachmentId": "CMS-2025-0240-0165-1",
            "commentId": "CMS-2025-0240-0165",
            "docketId": "CMS-2025-0240",
            "extractedMethod": "pypdf",
            "extractedText": "11921 Rockville Pike | Suite 300 | Rockville, MD 20852 301.881.3052 voice | 301.881.0898 fax | 800.638.8299 toll-free | 866.300.2900 Español Member: CFC 11404 | KidneyFund.org August 28, 2025 The Honorable Mehmet Oz Administrator Centers for Medicare and Medicaid Services"
        },
        {
            "attachmentId": "CMS-2019-0100-0177-1",
            "commentId": "CMS-2019-0100-0177",
            "docketId": "CMS-2019-0100",
            "extractedMethod": "pdfminer",
            "extractedText": "August 23, 2019 Seema Verma, MPH Administrator Centers for Medicare and Medicaid Services Department of Health and Human Services Room 445-G Attn: CMS-1711-P Hubert Humphrey Building 200 Independence Ave, SW Washington, DC 20201"
        },
        {
            "attachmentId": "CMS-2019-0100-0519-1",
            "commentId": "CMS-2019-0100-0519",
            "docketId": "CMS-2019-0100",
            "extractedMethod": "pdfminer",
            "extractedText": "Humana Inc. 500 W. Main St. Louisville, KY 40202-2946 www.humana.com September 9, 2019 Seema Verma, Administrator Centers for Medicare & Medicaid Services (CMS) 7500 Security Boulevard, Attention: CMS-1689-P Baltimore, MD 21244-1850"
        },
        {
            "attachmentId": "CMS-2019-0100-0205-1",
            "commentId": "CMS-2019-0100-0205",
            "docketId": "CMS-2019-0100",
            "extractedMethod": "pdfminer",
            "extractedText": "CMS-1711-P (July 18, 2019) proposes several significant changes for Home Health Provider community. A couple of these changes will have a negative impact on our industry's ability to provide care to the Medicare beneficiaries that are served across our nation."
        },
        {
            "attachmentId": "DEA-2024-0059-24062-1",
            "commentId": "DEA-2024-0059-24062",
            "docketId": "DEA-2024-0059",
            "extractedMethod": "pdfminer",
            "extractedText": "I am providing comments in support of the rescheduling of botanical cannabis (Docket No. DEA–1362). The Department of Health and Human Services appropriately concluded that cannabis has a currently accepted medical use and that its abuse potential does not warrant its placement as either a Schedule I or Schedule II controlled substance."
        }
    ]
    
    for i, extracted in enumerate(extracted_texts):
        client.index(index="comments_extracted_text", id=i, body=extracted)
    
    # Refresh indices
    client.indices.refresh(index="documents_text")
    client.indices.refresh(index="comments")
    client.indices.refresh(index="comments_extracted_text")
    
    print(f"✓ Ingested {len(documents)} documents")
    print(f"✓ Ingested {len(comments)} comments")
    print(f"✓ Ingested {len(extracted_texts)} comments (extracted text from attachments)")
    print("\nDockets included:")
    print("  DEA-2024-0059: 0 docs, 2 comments total")
    print("  CMS-2025-0240: 0 docs, 6 comments total")
    print("  CMS-2019-0100: 0 docs, 10 comments total")
    print("  CMS-2025-0001: 1 doc, 0 comments total")


if __name__ == "__main__":
    ingest_opensearch()
