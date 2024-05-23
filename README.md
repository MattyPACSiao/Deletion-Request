# Deletion-Request
### A python GUI that sends a request to site leadership to approve deletion of an exam/series/image.
![](https://github.com/MattyPACSiao/Deletion-Request/blob/main/img/mermaid-diagram-2024-02-23-142851.png)

### The Merge PACS application is able to run CLI commands and pass DICOM tags as command arguments from a macro icon. This python script is compiled into a `.exe` and ran on macro click.
- Takes input(patient info from DICOM tags taken from Merge RPACS) from the CLI.
- Takes input(tech name, and reason for deletion request) from user.
- Bundles the aforementioned input and injects it into a Google form URL to auto-populate and submit that form.
#### The following steps are external to this python script:
- A Google form submission sends our bundled data to a Google sheet.
- From the Google sheet, data is parsed and used to notify respective personnel of pending requests.

<br/><br/><br/><br/>
# SCSA RPACS Deletion Workflow

## Function Flow Chart 
[![](https://mermaid.ink/img/pako:eNptkcFqwzAMhl_F6NRC8wI5DNKkbJfBaHKbd9BsNQl1bOMohNL03efWOYxuPpnv-2Uk6wrKaYIcsiyTlns2lItX51pDovB-FLUKvWdpH_5k3Kw6DCyaSloRT_G5huuOiL8S3G8ktMRHN1fIuNlK2CZRJvFBYXTWkvmlqqSeCg6RDuhrMqSYdOOeS9cuRJa9iOWIs7g_sOzXPhIuQsDLUv7D1iHKxN5w7ESD34aWw9rUXwE7GCgM2Ov4add7TAJ3NJCEPF41hrMEaW8xhxO7-mIV5Bwm2sHkNTJVPbYBB8hPaMZISffswnvawmMZtx80KX32?type=png)](https://mermaid.live/edit#pako:eNptkcFqwzAMhl_F6NRC8wI5DNKkbJfBaHKbd9BsNQl1bOMohNL03efWOYxuPpnv-2Uk6wrKaYIcsiyTlns2lItX51pDovB-FLUKvWdpH_5k3Kw6DCyaSloRT_G5huuOiL8S3G8ktMRHN1fIuNlK2CZRJvFBYXTWkvmlqqSeCg6RDuhrMqSYdOOeS9cuRJa9iOWIs7g_sOzXPhIuQsDLUv7D1iHKxN5w7ESD34aWw9rUXwE7GCgM2Ov4add7TAJ3NJCEPF41hrMEaW8xhxO7-mIV5Bwm2sHkNTJVPbYBB8hPaMZISffswnvawmMZtx80KX32)
## Overview
1. Users submit a request to delete an exam via a Google form. 
2. This form contains relevant exam data and, on form submission, posts it to a Google sheet.
3. On the Google sheet each row represents a deletion request and contains relevant data
4. The Google sheet contains a script that does the following
    - Parses the requests
    - Sorts them by facility and request status
    - Builds Google forms for facility managers to the approve or reject deletion requests
        - Individual forms are built for each facility
    - Builds Google forms for PACS Admins to confirm deletion of exams
    - Emails the manager forms and PACS admin forms to the respective personnel based on facility
        - These emails are triggered to go out once a week 
## Script App
### Unit Tests
- `test.gs` contains unit tests for all functionality that does not involve user interaction ie form submission functionality. 
-  Run the function `fakeJest()` and the console will display what tests have passed or failed. This can provide more insight while debugging. Please make use of this if you make any changes to the code

### Form IDs
- This workflow makes use of 13 different forms:
    - A PACS admins' form for each of the 6 facilities 
        - These forms are for PACS admins to confirm the deletion of approved exams
    - A Managers' form for each of the 6 facilities 
        - These forms are for DMI managers to approve or reject deletion requests
    - A spare form used in the unit tests
- These are blank forms that get populated with relevant exam information every time an email is sent out and every time the form is submitted. This trigger happens with respect to individual facilities. 