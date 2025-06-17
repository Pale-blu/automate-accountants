# **Automate Accounts Developer Hiring Assessment**

This assessment is designed to evaluate your ability to build a system for processing scanned receipts automatically. The goal is to extract relevant details from PDF receipts using OCR/AI techniques and store the extracted data in a structured format.

## **Project Overview**

You will be working with a repository containing a collection of scanned receipts in **PDF format**, categorized into directories based on the year of purchase. The challenge is to **automate** the extraction of information from these scanned receipts and store it efficiently in a **SQLite database**.

Deadline for submission is **3 days** from when you receive the email.

## **Problem Statement**

Develop a solution as a **web application** with **REST APIs** that can:
1. **Upload scanned receipts** in PDF format. The files can be stored in a local directory.
2. **Validate** the uploaded files to ensure they are valid PDFs.
3. **Extract key details** from the receipts using **OCR/AI-based text extraction** techniques.
4. **Store extracted information** in a structured database schema.
5. **Provide APIs** for managing and retrieving receipts and their extracted data.

You may use **any programming language, framework, or OCR/AI library** to implement the solution.

---

## **Database Schema**

The extracted information should be stored in an **SQLite database (`receipts.db`)**.

### **1. Receipt File Table (`receipt_file`)**
Stores metadata of uploaded receipt files.

| Column Name     | Description                                                    |
|-----------------|----------------------------------------------------------------|
| `id`            | Unique identifier for each uploaded file                        |
| `file_name`     | Name of the uploaded file                                       |
| `file_path`     | Storage path of the uploaded file                               |
| `is_valid`      | Indicates if the file is a valid PDF                            |
| `invalid_reason`| Reason for file being invalid (if applicable)                   |
| `is_processed`  | Indicates if the file has been processed                        |
| `created_at`    | Creation time (when receipt was first uploaded)                 |
| `updated_at`    | Last update time (latest modification in case of re-upload)     |

### **2. Receipt Table (`receipt`)**
Stores extracted information from valid receipt files.

You can modify the schema as needed to store additional information extracted from the receipts like transaction details, purchased items details, payment details and other information.

| Column Name     | Description                                     |
|----------------|-------------------------------------------------|
| `id`           | Unique identifier for each extracted receipt     |
| `purchased_at` | Date and time of purchase (extracted from receipt)|
| `merchant_name`| Merchant name (extracted from receipt)           |
| `total_amount` | Total amount spent (extracted from receipt)      |
| `file_path`    | Path to the associated scanned receipt          |
| `created_at`   | Creation time (when receipt was processed)       |
| `updated_at`   | Last update time (latest modification)          |
---

## **API Specifications**

The solution should expose a set of **REST APIs** for receipt management. You may use any web framework and implement the APIs with or without an ORM.

### **1. `/upload` (POST)**
- Uploads a receipt file (PDF format only).
- Stores metadata in the `receipt_file` table.

### **2. `/validate` (POST)**
- Validates whether the uploaded file is a valid PDF.
- Updates `is_valid` and `invalid_reason` fields in the `receipt_file` table.

### **3. `/process` (POST)**
- Extracts receipt details using OCR/AI.
- Stores extracted information in the `receipt` table.
- Marks `is_processed` as `True` in the `receipt_file` table.

### **4. `/receipts` (GET)**
- Lists all receipts stored in the database.

### **5. `/receipts/{id}` (GET)**
- Retrieves details of a specific receipt by its ID.

---

## **Evaluation Criteria**

Your submission will be evaluated based on the following factors:

1. **Accuracy of extracted information** – How well the OCR/AI system extracts key details.
2. **Code quality & readability** – Clean, maintainable, and well-documented code.
3. **Database schema design** – Efficient and scalable schema structure.
4. **API design & functionality** – Proper implementation of API endpoints.
5. **Error handling & validation** – Robust handling of invalid files and extraction errors.
6. **Documentation** – Clear instructions on setup, usage, and functionality.
7. **Git commit history** – Meaningful commits showing structured development progress.

---

## **Submission Guidelines**

Your final submission should be a **ZIP file** containing:

1. **Source Code** – The complete implementation of your solution.
2. **Database File (`receipts.db`)** – The SQLite database with sample entries.
3. **Documentation** – A README file explaining:
   - How to set up and run the project
   - API usage with example requests/responses
   - Any dependencies required
4. **Execution Instructions** – Any specific setup steps needed to test your implementation.

---

## **Additional Notes**

1. **Flexibility** – You are free to enhance or modify the problem statement as needed. If you think of a better approach, feel free to implement it.
2. **Technology Choice** – Use any programming language, framework, and libraries of your choice.
3. **Duplicate Handling** – If the same receipt is uploaded multiple times, **update** the existing record instead of creating duplicates.
4. **Partial Submissions** – If your solution is incomplete or has bugs, **submit anyway**. We value your approach and thought process more than a perfect implementation.
5. **Support** – If you have any questions, feel free to reach out.

---

## **Happy Coding!**
