from langchain_core.output_parsers import StrOutputParser
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from operator import itemgetter
from langchain_community.document_loaders import UnstructuredMarkdownLoader

model = AzureChatOpenAI(azure_deployment="gpt-4o", api_version="2024-08-01-preview")
output_parser = StrOutputParser()

print("Please provide path (absolute path) of input design document")
#md_design_path = input()
md_design_path = "./design_review/design_doc.md"
print("Please provide path of review comments output file path")
#output_result_path = input()
output_result_path = "./design_review/DC_RC_110.md"
loader = UnstructuredMarkdownLoader(md_design_path)

design_doc_data = loader.load()
# design_doc_content = data[0].page_content

expert_engineer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            # Instruction

            You are an engineer with a lot of design experience. Please refer to the example of patterned processing flow for online processing design procedure and online processing design document, centralized management of derivation rule, and handling of special value (consideration), and review the design documents from the perspective of whether they follow the best practices and rules.
            Also, please generate review comments along with specific suggestions for improvement.
            
            ## Online processing design procedure

            * **Overview**  
             Extract online processing based on the deliverable "Screen design document" and design its specifications. Note that processing used in multiple use cases will be carried out in the sub-task "Common external design".  

            * **Input deliverable**  
            Architecture design work procedure, ER diagram (data model design), Table design document, Message design document, Screen design document, Screen transition diagram, External interface design document, Use case definition document, Common component design document, Common area design document, Performance and scalability study document, Form design document  

            * **Procedure**
            1. Extraction of online processing  
                Based on the deliverables "Use case definition document", "Screen transition diagram" and "Screen design document", extract online processing and summarize it in the deliverable "List of online processing".  

            2. Extraction of input/output items  
                Extract input/output items for processing from the deliverables "Screen design document", "Form design document" and "External interface design document".  

            3. Design of online processing  
                According to the deliverable "Architecture design work procedure", and based on the deliverables "Use case definition document", "Common component design document", and "Common area design document", design the following points for the online processing and describe them in the deliverable "Online processing design document".  
                * Control structure (branching, repetition, etc.)  
                * Input check  
                * Access to DB  
                * Scope of transaction  
                * Calculation  
                * Error handling  
                * Integration with external systems  
                * Input and output to file  
                * Exclusion control  
        
            4. Extraction of processing with performance risks
                Based on the deliverable "Performance and scalability study document", describe processes with performance risks (such as high workload or complex processing) in the remarks of the deliverable "List of online processing".  
                
            5. Add message
                If a new message (such as a screen message or log message) is required for each process, add the new message to the deliverable "Message design document".  

            6. Proposal for common components  
                If it is possible to standardize component in multiple processes, propose the common component to the person in charge of the task "Common internal design".  

            7. Confirmation of consistency with the data model  
                Check that the data items (item names, life cycles, etc.) handled in the online processing are consistent with the deliverables "ER diagram (data model design)" and "Table design document".  
            8. Addition to screen design document  
                If the items required for online processing design (such as hidden items) are not extracted as screen items, add them to the deliverable "Screen design document".  

            ## Example case of patternizing the processing flow of the online processing design document
When designing processing, the following advantages can be gained by focusing on the structure of the application and patterning the processing.  
　・ It is possible to standardize the granularity of descriptions (standardization of design documents by eliminating individuality)  
　・ It is possible to reduce the discrepancy in awareness between external design staff and internal design staff and beyond.  

The sample deliverable for the Online processing design document in the TERASOLUNA development procedure allows complete free description of the processing flow in order to increase versatility. However, when used in large-scale and complex systems, there is a risk of inconsistencies in the processing flow description and missing considerations. 
For this, it is effective to analyze the processing patterns provided by the project before designing, divide and pattern the processing flow accordingly, and if possible, reflect this in the deliverable format. 
Here, we will introduce one example of customization.  

#### Example of patternized processing flow of the online processing design document  

The assumed system covered by this case study is a web-based ordering system. In the online processing design document for this system, the application structure of the online processing is focused on, and one process is divided into nine procedures, and the format of the deliverables is also expressed in a tabular format to match the processing pattern.  


The content of each form is described below.
By using this form, it is intended to achieve "homogenization of design documents" and to define any discrepancies in awareness between the designer and the person in charge of the subsequent phase.  

  1. Overview  
     Depending on the screen state and user actions, define which procedure (stage in the table) to be executed for each execution pattern of the procedure in the process.

  2. Single-item check  
     A single-item check is a procedure for checking a single input item on the screen.

     The "error code" in the description item corresponds to the error message defined in the message definition document. If there is a replacement string in the message, it is defined as the "replacement string".  

  3. Correlation item check  
     The correlation item check is an input check procedure that targets multiple input items on the screen.

     In the "Check details" section of the description, define the combination of multiple screen items, and if the check result and item are edited, describe the editing details (in the example above, it shows that if the order date is not entered, the system date will be used).

  4. Acquisition  
     Acquisition is the procedure for acquiring data before updating in an updating process.

     In this format, mainly the inquiry contents to the DB are described.   
     If the "Error screen color change" box is checked in the description items, the color of the error part of the screen will change when an error occurs.  

  5. Master read  
     Master read is a procedure for acquiring master data.

     In this format, mainly the inquiry contents to the DB are described.   

  6. Business check  
     Business check is a procedure for checking data obtained through Acquisition and Master read.  

     It checks the input values and the values obtained through Acquisition and Master read. The "check details" section of the description items is presented in a table format to improve comprehensiveness.  

  7. Inquiry  
     The inquiry is a procedure that performs an inquiry (reference) to a DB, etc. in inquiry-type (reference-type) processing.

     The "sort order" in the description items indicates the priority for reordering the acquired data.

  8. Update  
     The update is a procedure that performs registration, updating, and deletion to DB, etc. in update-type processing.

     In the description items, the part "\#Details are..." in the above example describes the update conditions. However, if the conditions are complex, the details may be defined in a separate document, as in the above example.

  9. Output  
     Output is a procedure that performs form output and delayed start requests for the procedures implemented by inquiries and updates.

  10. Next screen item editing  
      Next screen item editing is a procedure for editing the content to be displayed on the next screen.  
      The details should match the display items defined in the screen design document shown below.  

#### Notes on applying this example  

This example is a good example of patterning, segmentation, and stylization, but please be careful when applying it to other projects, as there are the following points to note.

* This does not cover all processing patterns.
                
## Selecting the design part (business logic and input value check)
### Selecting the design part (business logic and input value check)

There are two options for input check in web applications: client-side script-based and server-side input check. In rich clients, business logic and input check can be placed on both the client and server sides. This section explains what each of these options means and how they should be used.

* **Business logic (Rich client)**  
  In rich clients, it is recommended to place the business logic that performs actual business processing, such as accessing the DB, on the server side. For this reason, the business logic on the client side usually only performs communication with the server. However, for processing that is completed on the client side, the business logic on the client side includes the business processing. Processing that is completed on the client side includes the following.

  * Printing forms

  * Recalculation processing that can be done on the client side only

  * Saving setting information, etc. on the client PC

  * Reading information from resources on the client PC

* **Input check (Web browser)**  
  In web application, in addition to input check on the server side, input check on the client side using client-side script is also possible. By performing input check on the client side, users can find errors before accessing the server, which helps improve usability.   
  However, input check on the client side is meaningless if the client has disabled scripts or if an HTTP request is issued directly to the server, so even if you perform input check on the client side, you should always perform input check on the server side.

* **Input check (Rich client)**  
  Client-side input check should always be performed from the perspective of application usability. When an error occurs, it is necessary to provide feedback that allows the user to determine which item has caused the error and why. When performing client-side input check, there are two main methods as follows.

  * Perform input check of the entire screen when the registration button is pressed.

  * Perform single-item check of the relevant field when the field value is changed or when the focus is lost.

  The former input check should always be performed, but the latter is not always necessary. However, it improves usability because it provides feedback that an error has occurred during input.  
  Server-side input check should always be performed because it has a security aspect of preventing the server from accepting unintended messages from unauthorized clients. Even if a check error occurs, it should not return the error details to avoid providing hints for attacks. In addition, if the input check requires DB access and cannot be checked by the client alone, an input check on the server side is required. In this case, the input check is performed as part of the business process, so information such as error items and error details should be returned so that appropriate feedback can be provided on the client side.

* **Input value check should be implemented on the server side**  
  Regardless of whether or not input check is performed on the client side, input check should be implemented on the server side. This is because most systems are vulnerable to external threats, and client-side check alone is not sufficient to deal with external threats. Even if a system does not have external connections, it may have external connections due to changes in the operating environment, etc.  
  The following explains the necessity of server-side check using the example of using SSL communication.

  In this example, the client accesses the application server using SSL communication. The communication itself is encrypted using SSL, and is protected from threats such as eavesdropping. It also avoids threats such as requests being falsified. However, it cannot protect against threats such as unauthorized requests from the client side. If the client side checks are performed, it is possible to prevent unauthorized requests being sent when valid operations are performed. However, it is not possible to prevent unauthorized requests without performing valid operations. In other words, client-side checks do not contribute much to the robustness of the system. It is better to limit the purpose of client-side checks to improving usability.  
  As in this example, if there is a discussion about not performing input value checks on the server side, it is important to understand the reasons behind this and check the validity of these reasons.

  ## Centralized management of derivation rule

* **Standardize the derivation rules and centrally manage design and implementation**

  In systems, there are many cases where calculations are performed based on the data being handled and respond. For example, there are various cases, such as those related to numerical values, such as aggregation, yen conversion, and N business days before, as well as rules to get them when the product code includes large, medium, and small classification codes. If such rules are implemented individually for each business, it will take extra man-hours for testing and specification changes, and it may cause discrepancies in the results.  
  Such derivation rules should be designed and implemented for common use rather than implementing them individually. By designing and implementing them as common processes, it is possible to not only reduce the man-hours required for individual implementation, but also improve quality and maintainability.  
  In order to benefit from this kind of commonality, it is necessary to ensure that common processes are used in individual processes, and to provide appropriate expansion methods. For this reason, it is necessary to centrally manage design and implementation, and to be able to promote the use of common processes and extract requirements.

  ## Handling of special value (consideration)

* **When generating special values, consider how to achieve them when designing**  

    In business processes, there are various situations to generate various values, such as keys to identify specific information or codes composed of special values. Although such business rules for generating values can be easily described in specifications, some of them are very difficult to implement.  
    For example, consider the following rule.  

    * Issue sequential numbers  

    * Make sure there are no missing numbers  

    While it is certainly easy to describe in specifications, it is quite difficult to implement. For example, if you consider using an oracle sequence, it is possible to issue sequential numbers, but there might be missing numbers. In the case of locking the table and counting all records, you need to consider whether it will affect performance. Furthermore, if you add more specific rules, it may become difficult to implement.  
    When generating values according to business rules, you should always check that there is a suitable way to achieve this. And, it is a good idea to create patterns in your project for reusable items that do not depend on specific business rules.  
            """,
        ),
        ("human", "{design_document}"),
    ]
)

expert_engineer_chain = expert_engineer_prompt | model | output_parser

business_engineer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            # Instruction

            You are an engineer with a lot of knowledge about this system. Please review the design documents based on the each requirement definition document and comment on them with specific suggestions for improvement.

            ## Business rule definition

            # Business rule definition document

| Item    | Content        |
|-------|-----------|
| System name | QAA system   |
| Created by   | Shota Oki      |
| Created on   | 2024/5/21 |
| Updated by   | Ibu Ueno      |
| Updated on   | 2024/8/29 |

## BR_B01_01: Maturity level calculation

### Content of the rule

#### (1) How to calculate maturity level

Based on the answers to the questions on the check sheet, calculate the maturity level using the following method.

* The information below is based on the cell functions of the Quick Assessment Check Sheet as of the date of publication of this document.

- The maturity level for each management area is defined as 1 to 5. However, the personnel management area is defined as 1 to 4.
- For Lv X, the score is (X-1)+(question response rate/level achievement criteria).
- If the response rate for questions of Lv 1 is equal to or greater than the level achievement criteria, the maturity level is 1.<br>
    - For Lv 1 questions, a response of "TRUE" means that it has not been achieved, and a response rate that is equal to or greater than the achievement criteria means that Lv 1 has not been achieved.
- If the response rate for questions of Lv 1 does not exceed the level achievement criteria, the maturity level will be the score of the level +1 with the highest response rate that exceeds the level achievement criteria.

***
Improvement idea for calculating the maturity level
- The above calculation method for the maturity level for Lv 1 is difficult to understand as follows.
    - Exceeding the achievement criteria means that the project management has not been advanced (it has not been advanced).
    - Falling below the achievement criteria means that the project management has been advanced (it has been advanced).
- The following two are proposed as improvements
    - Count the number of "FALSE" instead of "TRUE" only for Level 1 maturity, and change the achievement criteria to ( 1 - original achievement criteria)<br>
    →For any level of maturity, it can be understood that "the response rate is equal to or greater than the achievement criteria = it has been advanced".
    - Change the questions for Level 1 maturity in the self-check tool<br>
    →For all maturity levels, it can be understood that "the response rate for TRUE answers is above the achievement standard = it has been advanced".
- As of today, there is a possibility that the manual Excel sheet and the QAA system will be used together in the future, and if the logic is different, it could cause confusion, so the logic has been adjusted to match the Excel sheet.
- If the operation of the Quick Assessment is improved in the future, the QAA system will also be modified.
***

#### (2) Level achievement criteria

The level achievement criteria for each maturity level in each management area are defined in tables 1 to 6 below.

* The information below is based on the cell functions of the Quick Assessment Check Sheet as of the date of publication of this document.

Table 1 Quality management Maturity level achievement criteria

| Maturity level | Level achievement criteria |  
|-------|---------|  
| 1     | 20%     |  
| 2     | 100%    |  
| 3     | 100%    |  
| 4     | 75%     |  
| 5     | 80%     |  

Table 2 Progress management Maturity level achievement criteria

| Maturity level | Level achievement criteria |  
|-------|---------|  
| 1     | 20%     |  
| 2     | 100%    |  
| 3     | 100%    |  
| 4     | 66%     |  
| 5     | 75%     |  

Table 3 Problem/issue management Maturity level achievement criteria

| Maturity level | Level achievement criteria |  
|-------|---------|  
| 1     | 20%     |  
| 2     | 100%    |  
| 3     | 80%     |  
| 4     | 100%    |  
| 5     | 75%     |  

Table 4 Configuration management Maturity level achievement criteria

| Maturity level | Level achievement criteria |  
|-------|---------|  
| 1     | 20%     |  
| 2     | 100%    |  
| 3     | 85%     |  
| 4     | 75%     |  
| 5     | 100%    |  

Table 5 Risk management Maturity level achievement criteria

| Maturity level | Level achievement criteria |  
|-------|---------|  
| 1     | 20%     |  
| 2     | 100%    |  
| 3     | 100%    |  
| 4     | 100%    |  
| 5     | 100%    |  

Table 6 Personnel management Maturity level achievement criteria

| Maturity level | Level achievement criteria |  
|-------|---------|  
| 1     | 20%     |  
| 2     | 100%    |  
| 3     | 100%    |  
| 4     | 100%    |  
| 5     | 100%    |  

#### (3) Calculation method of response rate

- The response rate for questions of maturity level X in each management area is calculated as follows.<br>
```Response rate for questions of maturity level X = (number of questions of maturity level X with check set to TRUE) / (number of questions of maturity level X)```

---

## BR_B01_02: Advancement Lv calculation

### Content of the rule

#### (1) Calculation criteria for advancement level

The advancement level is calculated based on the maturity level of each management area of the project, using the following criteria.

- If the maturity level is 4 or higher, the advancement level is 2.
- If the maturity level is between 2 and 4, the advancement level is 1.
- If the maturity level is less than 2, the advancement level is 0.

#### (2) Table of advancement Lv

Table 1 shows the maturity levels and criteria used to calculate advancement Lv.

Table 1 Calculation criteria for advancement level

| Range of maturity level | Advancement Lv |  
|----------|-------|  
| 4 or higher      | 2     |  
| between 2 and 4   | 1     |  
| less than 2      | 0     |  

#### (3) Supplemental

- The Advancement Lv is an indicator of the maturity of the project, and is calculated based on the status of the project's efforts in terms of progress management and quality management.
- The calculation of the maturity level follows the separately defined "[BR_B01_01: Maturity level calculation] (#br_b01_01Maturity level calculation)".

---

## BR_B01_03: Output of consideration draft

### Content of the rule

#### (1) Maturity level evaluation

- The maturity level is calculated based on the response rate to the check sheet, in accordance with the "[BR_B01_01: Maturity level calculation](#br_b01_01Maturity level calculation)" business rule.
- The calculation method for the maturity level is determined by whether or not the response rate to the questions for each level exceeds the level achievement criteria.

#### (2) Output of consideration

- Based on the answers to the check sheet in each management area and the maturity level, the generative AI outputs the consideration in text format.
- When outputting, evaluate the maturity of the management area of the project and summarize the consideration according to the prompt template "[BR_P01_03](./prompt/BR_P01_03.txt)".

---

## BR_B01_04: Output of improvement measure draft

### Content of the rule

#### (1) Maturity level evaluation

- The maturity level is calculated based on the response rate to the check sheet, in accordance with the "[BR_B01_01: Maturity level calculation](#br_b01_01Maturity level calculation)" business rule.
- The calculation method for the maturity level is determined by whether or not the response rate to the questions for each level exceeds the level achievement criteria.

#### (2) Output of improvement measure

- Based on the answers to the check sheet in each management area, the maturity level and consideraion, the generative AI outputs the consideration in text format.
- When outputting, evaluate the maturity of the management area of the project and output the improvement measure according to the prompt template "[BR_P01_04](./prompt/BR_P01_04.txt)".

---

## BR_B01_05: Output of support schedule draft

### Content of the rule

#### (1) Output of support schedule draft

- Based on the consideration and improvement measures for the project status derived from the answers to the check sheet, output a draft schedule to support the improvement of the project status.
- Considering automatic output using generative AI, the output format is Mermaid.

#### (2) Lineup of support schedule

- The following is a list of the support services that will be included in the support schedule, along with a overview of each.
    -
        1. Assessment and improvement concept creation: Conduct a detailed assessment and propose an improvement concept based on the results.
    -
        2. PMO support service: Review each management process with the assumption of introducing a tool, and try to make it lighter.
    -
        3. Data collection and analysis support service: Build a real-time monitoring system by applying tools.
    -
        4. Primary information utilization support service: Utilize primary information from development work to solve project management issues.

- Item 1 is always included in the support schedule.
- Items 2 to 4 will be included in the lineup as necessary depending on the project situation.
- The number of man-months required for each lineup will be stated in units of "X people/month". The value of X will be calculated by the generative AI based on the maturity level and the improvement measures to be implemented.

#### (3)Image of support schedule

- The image of the support schedule output by Mermaid is shown below.

```mermaid
gantt  
dateFormat  YYYY-MM

title ADM support schedule 
  
section 1. Assessment and improvement concept creation
4.5 people/month:adm_0, 2024-05, 2.5M

section 2. PMO support service
2 people/month:adm_0, 2024-07, 2M

section 3. Data collection and analysis support service
2 people/month:adm_0, 2024-08, 2M

section 4. Primary information utilization support service
2 people/month:adm_0, 2024-09, 2M
```

---

## BR_B01_06: Output of radar chart

### Content of the rule

#### (1) Format of radar chart

- The radar chart to visualize the maturity level of each management area is output in the format shown in the image below.

![Radar chart image](./img/Radar chart legend.png)

#### (2) Supplemental

- The maturity levels for each management area that are reflected in the radar chart are based on the separately defined "[BR_B01_01: Maturity level calculation] (#br_b01_01Maturity level calculation)".

---

## BR_B01_07: Calculation of target level

### Content of the rule

#### (1) Update the response status of the check sheet

- If the value of the "check" item on the check sheet is updated when the improvement measures are implemented, calculate the maturity level based on the updated response status of the check sheet.

#### (2) Computation of advancement level after updating the response status of the check sheet

- Calculate the advancement level based on the maturity level after the check sheet response status is updated.

#### (3) Supplemental

- The maturity level for each management area follows the separately defined "[BR_B01_01: Maturity level calculation] (#br_b01_01Maturity level calculation)".
- The advancement level for each management area follows the separately defined "[BR_B01_02: Advancement level calculation] (#br_b01_02 Advancement level calculation)".

---

## BR_B01_08: Automatic numbering of project ID  
   
### Content of the rule  
   
#### (1) Automatic numbering of project ID  
   
- Project IDs are automatically assigned by the system.  
- The project IDs assigned are 6-digit sequential numbers following "PJ" (e.g. PJ000001).  
- The sequential number will increase by 1 each time a new project is registered.  
   
#### (2) Exception handling for numbering  
   
- Project IDs that have already been used will not be reused.  
- If the maximum number (PJ999999) is reached, new projects will not be accepted.  

#### BR_B01_09: Output of result file  
   
##### Content of the rule  
   
###### (1) Output of result file  
   
- The QAA system outputs the results of the maturity level and advancement level of management on the screen and also allows them to be downloaded as files.  
- The file format is PDF and includes the following information.  
    - Project ID  
    - Maturity level  
    - Advancement level of management  
    - Proposed service  
   
###### (2) File name format  
   
- The name of the output file is "Project ID_Maturity level_Advancement level.pdf".  
   
###### (3) How to download  
   
- Place a "Download Results" button on the results screen so that users can download files by clicking on it.

            ## Overview workflow diagram

Quick Assessment can be used by the organization to be supported.
Cross-sectional analysis and report creation are achieved using accumulated knowledge.

```plantuml
@startuml  
title Final version
autonumber

actor "Organization to be supported_Main department" as Support_Org_Department  
actor "Organization to be supported_Representative" as Support_Org_Staff  
actor "ADM technlogy department_Contact point" as ADM_Tech_Window  
actor "ADM technlogy department_Reviewer" as ADM_Tech_Reviewer  
actor "ADM technlogy department_Representative" as ADM_Tech_Staff  
participant "QAA system" as QAA_System  
participant "Generative AI" as Gen_AI  
database "QAA knowledge base" as Past_Data 

== Quick assessment implementation ==
ADM_Tech_Window -> Support_Org_Department :  Send QAA system usage guideline 
Support_Org_Department -> Support_Org_Staff : Request to use QAA system
Support_Org_Staff -> QAA_System : Access and answer self-check tool
QAA_System -> Gen_AI : Input assessment results into generative AI
Gen_AI -> Past_Data : Acquire past similar data
Past_Data -> Gen_AI : Return past similar data
Gen_AI -> QAA_System : Return assessment results \nwith reference to past data
QAA_System -> Support_Org_Staff : Output assessment results
note over Support_Org_Staff #fadbda : FID1. Assessment results (PDF format)   
Support_Org_Staff -> Support_Org_Department : Submission (FID1)


== Feedback registration ==
note left QAA_System : A few days after outputting the assessment results is assumed
QAA_System -> Support_Org_Department : Send an email requesting feedback registration for the output results

Support_Org_Department -> QAA_System : Register feedback
QAA_System -> Past_Data : Store feedback

== Interview on additional requirement ==
note left QAA_System : A few days after outputting the assessment results is assumed\n* Need to consider whether to do this at the same time as sending the feedback registration request email.
QAA_System -> Support_Org_Department : Send an email to ask for a meeting to discuss additional requirement
QAA_System -> ADM_Tech_Window : Notification of sending an email to ask for a meeting to discuss additional requirement
QAA_System -> ADM_Tech_Reviewer : Notification of sending an email to ask for a meeting to discuss additional requirement

group Check the validity and evidence of the assessment results\n* Conduct as necessary, such as receiving a call from the business unit or wishing to contact them
ADM_Tech_Reviewer -> QAA_System : Access
QAA_System -> Past_Data : Acquire assessment results and similar case results
Past_Data -> QAA_System : Return assessment results (including evidence for consideration) and similar case results
QAA_System -> ADM_Tech_Reviewer : Check validity and evidence from assessment results
end

alt Pull type (when contacted by the business unit)
  Support_Org_Department -> ADM_Tech_Window : Consult on additional requirements (additional assessment, support, etc.)
else Push type (when contacting from our side)
  ADM_Tech_Reviewer -> Support_Org_Department : Consult on additional requirements (additional assessment, support, etc.)
end

ADM_Tech_Reviewer -> QAA_System : Register the results of the additional requirement interview
note over QAA_System : t is assumed that a system similar to the Quick Assessment will be built, but the details will be considered separately\n* Wish to achieve this in FY24
QAA_System -> ADM_Tech_Reviewer : Use generative AI to output issues and improvement proposals from the interview results


== Analysis and report creation ==
ADM_Tech_Reviewer -> QAA_System : Access and search for past data
note right QAA_System : Consider separately whether to use BI tools or to create an analysis function for the QAA system with administrator permission
QAA_System -> Past_Data : Search for past data
Past_Data -> QAA_System : Return past data
QAA_System -> ADM_Tech_Reviewer : Output analysis result and report

@enduml 
```

            ## Non-functional requirement definition

| Item No.   | Catergory          | Subcatergory         | Specific requirement from customer                           |
|------|--------------|-------------|---------------------------------------|
| A.1  | Availability          | Continuity         | -                                     |
| A.2  | Availability          | Fault tolerance        | Although high fault tolerance is not required, basic monitoring and alert functions should be set. |
| A.3  | Availability          | Disaster control        | -                                     |
| A.4  | Availability          | Recoverability         | -                                     |
| B.1  | Performance and scalability       | Amount of work processed       | -                                     |
| B.2  | Performance and scalability       | Performance target value       | Even with function that uses Generative AI, the result must be output within 120 seconds.          |
| B.3  | Performance and scalability       | Resource scalability     | The design should allow for scaling up and out of Azure as needed. |
| B.4  | Performance and scalability       | Performance quality assurance      | -                                     |
| C.1  | Operability and maintainability       | Normal operation        | Provide a UI for PC web browser, and enable access with secure FAT/BXO. |
| C.2  | Operability and maintainability       | Maintenance operation        | Monitor and manage systems via the Azure portal            |
| C.3  | Operability and maintainability       | Operation during failure       | Send notifications by email when failure occurs.                       |
| C.4  | Operability and maintainability       | Operating environment        | Use Azure's standard operating environment.                   |
| C.5  | Operability and maintainability       | Support structure      | Support is provided during normal business hours.                     |
| C.6  | Operability and maintainability       | Other operation management policies  | -                                     |
| D.1  | Transitivity          | Transition period        | -                                     |
| D.2  | Transitivity          | Transition method        | -                                     |
| D.3  | Transitivity          | Transition target (device)    | -                                     |
| D.4  | Transitivity          | Transition target (data)   | -                                     |
| D.5  | Transitivity          | Transition plan        | -                                     |
| E.1  | Security       | Precondition and restriction   | -                                     |
| E.2  | Security       | Security risk analysis | -                                     |
| E.3  | Security       | Security diagnosis    | -                                     |
| E.4  | Security       | Security risk management | -                                     |
| E.5  | Security       | Access and usage restrictions   | Authentication using Azure Active Directory.      |
| E.6  | Security       | Data confidentiality      | Encrypt communications using HTTPS.                    |
| E.7  | Security       | Fraud tracking and monitoring     | Save the output results of generative AI on Azure so that they can be used for investigations such as unauthorized access. |
| E.8  | Security       | Network measures    | Restrict access only via ZScaler. |
| E.9  | Security       | Malware measures     | -                                     |
| E.10 | Security       | Web measures       | -                                     |
| F.1  | System environment and ecology | System restrictions and preconditions | Assumes the use of Azure services.               |
| F.2  | System environment and ecology | System characteristics      | Minimize maintenance effort by using Azure PaaS services. |
| F.3  | System environment and ecology | Conforming standards        | -                                     |
| F.4  | System environment and ecology | Equipment installation environment conditions    | -                                     |
| F.5  | System environment and ecology | Environmental management   | -                                     |

            """,
        ),
        ("human", "{design_document}"),
    ]
)

business_engineer_chain = business_engineer_prompt | model | output_parser

tech_lead_engineer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a tech lead engineer. Please review from a technical perspective, such as service-oriented architecture, and provide review comments.",
        ),
        ("human", "{design_document}"),
    ]
)

tech_lead_engineer_chain = tech_lead_engineer_prompt | model | output_parser

supervisor_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are the team leader. Please organize the review comments from each engineer about {design_document} to ensure consistency.
            """,
        ),
        (
            "human",
            """
            Review comment from engineer with lots of design experience:{expert_engineer}¥n
            Review comment from engineer with lots of knowledge of the business of this system:{business_engineer}¥n
            Review comment from tech lead engineer:{tech_lead_engineer}
            """,
        ),
    ]
)

supervisor_chain = (
    RunnableParallel(
        expert_engineer=expert_engineer_chain,
        business_engineer=business_engineer_chain,
        tech_lead_engineer=tech_lead_engineer_chain,
        design_document=itemgetter("design_document"),
    )
    | supervisor_prompt
    | model
    | output_parser
)
review_comments = supervisor_chain.invoke({"design_document": design_doc_data})


review_score_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Please evaluate review comments {review_comments} collected by team leader on a score from 1 to 10 impacting design document {design_document} flow
            Feedback and score:
            """,
        ),
        (
            "human",
            """
            Collective score for review comment collected by team leader:{team_leader}
            """,
        ),
    ]
)
review_score_chain = (
    RunnableParallel(
        team_leader=supervisor_chain,
        review_comments=itemgetter("review_comments"),
        design_document=itemgetter("design_document"),
    )
    | review_score_prompt
    | model
    | output_parser
)

review_comments_score = review_score_chain.invoke(
    {"design_document": design_doc_data, "review_comments": review_comments}
)


with open(output_result_path, "w") as f:
    print(review_comments, file=f)
    print("-----------------------", file=f)
    print(review_comments_score, file=f)
    f.close()

print(review_comments)
print(review_comments_score)
