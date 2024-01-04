# Deletion-Request
### A python GUI that sends a request to site leadership to approve deletion of an exam/series/image.
![](https://github.com/MattyPACSiao/Deletion-Request/blob/main/img/Del.png)

### The Merge PACS application is able to run CLI commands and pass DICOM tags as command arguments from a macro icon. This python script is compiled into a `.exe` and ran on macro click.
- Takes input(patient info from DICOM tags taken from Merge RPACS) from the CLI.
- Takes input(tech name, and reason for deletion request) from user.
- Bundles the aforementioned input and injects it into a Google form URL to auto-populate and submit that form.
#### The following steps are external to this python script:
- A Google form submission sends our bundled data to a Google sheet.
- From the Google sheet, data is parsed and used to notify respective personnel of pending requests.