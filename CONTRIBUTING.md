<!--
SPDX-FileCopyrightText: 2026 Zoe Nickson <zoe.nickson@sidingsmedia.com>
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Contributing

## Getting started

The backend system is built using Python with poetry.

### Pre-commit

This project uses [pre-commit](https://pre-commit.com/) to run
pre-commit hooks to ensure correct formatting of code. Make sure you
have installed pre-commit and then run `pre-commit install` to set up
the hooks.

## Design

The following notes are a rough design / plan for initial work.

### Endpoints

<!--
Input to https://diagon.arthursonzogni.com/#Tree

/
  accounts/
    POST - Create new bank account
    {id}/
      GET - Get account details
      PATCH - Partial update account details
      DELETE - Delete this bank account
      statements/
        GET - Get list of statements. Will include filtering options (e.g. tax year)
        POST - Create a new statement by passing the details as JSON
        {id}/
          GET - Get statement. Alias of GET /statements/{id}
          PATCH - Partial update of statement. Alias of PATCH /statements/{id}
          DELETE - Delete the statement. This will delete the linked file. Alias of DELETE /statements/{id}
          file/
            GET Get the PDF of the statement. Alias of GET /statements/{id}/file
            PUT Add or replace the PDF statement. Alias of PUT /statements/{id}/file
            DELETE Delete the PDF statement. Alias of DELETE /statements/{id}/file
        file/
          POST - Create new statement from a PDF file
  banks/
    POST - Create a new bank
    {id}/
      GET - Get this bank
      PATCH - Partial update for this bank
      DELETE - Delete this bank account. Will fail if there are accounts currently under this bank.
      accounts/
        GET - Get all accounts under this bank
  statements/
    GET - Get list of statements. Includes filtering (e.g. tax year)
    {id}/
      GET - Get JSON representation of statement
      PATCH - Partial update statement
      DELETE - Delete this statement. Will deleted any linked file
      file/
        GET Get the PDF of the statement
        PUT Add or replace the PDF statement
        DELETE Delete the PDF statement
    employments/
    POST - Create a new employment
    {id}/
      GET - Get employment details
      PATCH - Partial update of employment
      DELETE - Delete this employment. Will delete linked files
      files/
        POST - Upload additional employment file
        {id}/
          GET - Download linked file
          DELETE - Delete linked file
      payslips/
        GET - Get payslips associated with this employment. Includes filtering
        POST - Create a new payslip by passing details as JSON
        {id}/
          GET - Get a payslip. Alias of GET /payslips/{id}
          PATCH - Partial update payslip. Alias of PATCH /payslips/{id}
          DELETE - Delete this payslip. Will delete any linked file. Alias of DELETE /payslips/{id}
          file/
            GET - Get PDF linked to this payslip. Alias of GET /payslips/{id}/file
            PUT - Add or replace the PDF payslip. Alias of PUT /payslips/{id}/file
            DELETE - Delete this linked file
         file
           POST - Create payslip from PDF
  payslips
    GET - Get all payslips. Includes filtering
    {id}
      GET - Get this payslip
      PATCH - Partial update payslip
      DELETE - Delete this payslip. Will delete any linked file.
      file/
        GET - Get PDF linked to this payslip
        PUT - Add or replace the PDF payslip
        DELETE - Delete this linked file
  income/
    GET - Summary of income by tax year.
    {tax year}/
      GET - Summary of income for this tax year by month.
      {tax month}/
        GET - Summary of income for this tax month
  tax/
    GET - Summary of tax by tax year.
    {tax year}/
      GET - Summary of tax by month. Includes filtering.
      {tax month}/
        GET - Summary of tax for this month.
      allowance/
        personal/
          PUT - Modify the personal allowance
          GET - Get the personal allowance
        savings/
          PUT - Modify the savings allowance
          GET - Get the savings allowance
    bands/
      {tax year}/
        POST - Create new tax band
        {id}/
          DELETE - Delete tax band
-->

```
/
 ├─accounts/
 │  ├─POST - Create new bank account
 │  └─{id}/
 │     ├─GET - Get account details
 │     ├─PATCH - Partial update account details
 │     ├─DELETE - Delete this bank account
 │     └─statements/
 │        ├─GET - Get list of statements. Will include filtering options (e.g. tax year)
 │        ├─POST - Create a new statement by passing the details as JSON
 │        ├─{id}/
 │        │  ├─GET - Get statement. Alias of GET /statements/{id}
 │        │  ├─PATCH - Partial update of statement. Alias of PATCH /statements/{id}
 │        │  ├─DELETE - Delete the statement. This will delete the linked file. Alias of DELETE /statements/{id}
 │        │  └─file/
 │        │     ├─GET Get the PDF of the statement. Alias of GET /statements/{id}/file
 │        │     ├─PUT Add or replace the PDF statement. Alias of PUT /statements/{id}/file
 │        │     └─DELETE Delete the PDF statement. Alias of DELETE /statements/{id}/file
 │        └─file/
 │           └─POST - Create new statement from a PDF file
 ├─banks/
 │  ├─POST - Create a new bank
 │  └─{id}/
 │     ├─GET - Get this bank
 │     ├─PATCH - Partial update for this bank
 │     ├─DELETE - Delete this bank account. Will fail if there are accounts currently under this bank.
 │     └─accounts/
 │        └─GET - Get all accounts under this bank
 ├─statements/
 │  ├─GET - Get list of statements. Includes filtering (e.g. tax year)
 │  ├─{id}/
 │  │  ├─GET - Get JSON representation of statement
 │  │  ├─PATCH - Partial update statement
 │  │  ├─DELETE - Delete this statement. Will deleted any linked file
 │  │  └─file/
 │  │     ├─GET Get the PDF of the statement
 │  │     ├─PUT Add or replace the PDF statement
 │  │     └─DELETE Delete the PDF statement
 │  ├─employments/
 │  ├─POST - Create a new employment
 │  └─{id}/
 │     ├─GET - Get employment details
 │     ├─PATCH - Partial update of employment
 │     ├─DELETE - Delete this employment. Will delete linked files
 │     ├─files/
 │     │  ├─POST - Upload additional employment file
 │     │  └─{id}/
 │     │     ├─GET - Download linked file
 │     │     └─DELETE - Delete linked file
 │     └─payslips/
 │        ├─GET - Get payslips associated with this employment. Includes filtering
 │        ├─POST - Create a new payslip by passing details as JSON
 │        └─{id}/
 │           ├─GET - Get a payslip. Alias of GET /payslips/{id}
 │           ├─PATCH - Partial update payslip. Alias of PATCH /payslips/{id}
 │           ├─DELETE - Delete this payslip. Will delete any linked file. Alias of DELETE /payslips/{id}
 │           ├─file/
 │           │  ├─GET - Get PDF linked to this payslip. Alias of GET /payslips/{id}/file
 │           │  ├─PUT - Add or replace the PDF payslip. Alias of PUT /payslips/{id}/file
 │           │  └─DELETE - Delete this linked file
 │           └─file
 │              └─POST - Create payslip from PDF
 ├─payslips
 │  ├─GET - Get all payslips. Includes filtering
 │  └─{id}
 │     ├─GET - Get this payslip
 │     ├─PATCH - Partial update payslip
 │     ├─DELETE - Delete this payslip. Will delete any linked file.
 │     └─file/
 │        ├─GET - Get PDF linked to this payslip
 │        ├─PUT - Add or replace the PDF payslip
 │        └─DELETE - Delete this linked file
 ├─income/
 │  ├─GET - Summary of income by tax year.
 │  └─{tax year}/
 │     ├─GET - Summary of income for this tax year by month.
 │     └─{tax month}/
 │        └─GET - Summary of income for this tax month
 └─tax/
    ├─GET - Summary of tax by tax year.
    ├─{tax year}/
    │  ├─GET - Summary of tax by month. Includes filtering.
    │  ├─{tax month}/
    │  │  └─GET - Summary of tax for this month.
    │  └─allowance/
    │     ├─personal/
    │     │  ├─PUT - Modify the personal allowance
    │     │  └─GET - Get the personal allowance
    │     └─savings/
    │        ├─PUT - Modify the savings allowance
    │        └─GET - Get the savings allowance
    └─bands/
       └─{tax year}/
          ├─POST - Create new tax band
          └─{id}/
             └─DELETE - Delete tax band
```

### Packages

The endpoints above can be grouped into the following packages.

- accounts
  - Handles CRUD of bank accounts
  - Includes the following endpoint groups:
    - accounts
    - banks
- statements
  - Handles CRUD of statements including processing of PDFs
  - Includes the following endpoint groups:
    - statements
- employments
  - Handles CRUD of employments
  - Includes the following endpoint groups:
    - employments
- payslips
  - Handles CRUD of employments including processing of PDFs
  - Includes the following endpoint groups:
    - payslips
- tax
  - Handles tax calculations
  - Includes the following endpoint groups:
    - income
    - tax

## DCO

All contributions (including pull requests) must agree to the Developer
Certificate of Origin (DCO) version 1.1. This is exactly the same one
created and used by the Linux kernel developers and posted on
[http://developercertificate.org/](http://developercertificate.org/). A
copy of this can also be found in the project root (DCO_V1.1). This is a
developer's certification that they have the right to submit the patch
for inclusion into the project. Simply submitting a contribution implies
this agreement, however, please include a "Signed-off-by" tag in every
patch (this tag is a conventional way to confirm that you agree to the
DCO).
