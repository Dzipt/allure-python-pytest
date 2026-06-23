from pathlib import Path

FEATURES = {
    "accounts": [
        "customer_can_view_account_details",
        "customer_can_download_statement",
        "customer_can_filter_transactions",
        "customer_can_search_transaction_history",
        "customer_can_view_account_balance",
        "customer_can_view_account_currency",
        "customer_can_view_account_iban",
        "customer_can_rename_account",
        "customer_can_archive_account",
        "customer_can_restore_account",
    ],
    "cards": [
        "cardholder_can_block_card",
        "cardholder_can_unblock_card",
        "cardholder_can_change_pin",
        "cardholder_can_view_card_limits",
        "cardholder_can_enable_online_payments",
        "cardholder_can_disable_online_payments",
        "cardholder_can_view_card_details",
        "cardholder_can_replace_card",
        "cardholder_can_set_spending_limit",
        "cardholder_can_view_card_transactions",
    ],
    "payments": [
        "customer_can_make_internal_transfer",
        "customer_can_make_external_transfer",
        "customer_can_pay_utility_bill",
        "customer_can_schedule_payment",
        "customer_can_cancel_scheduled_payment",
        "customer_can_repeat_payment",
        "customer_can_save_payment_template",
        "customer_can_delete_payment_template",
        "customer_can_view_payment_status",
        "customer_can_download_payment_receipt",
    ],
    "transfers": [
        "customer_can_transfer_between_own_accounts",
        "customer_can_transfer_to_saved_beneficiary",
        "customer_can_add_beneficiary",
        "customer_can_delete_beneficiary",
        "customer_can_edit_beneficiary",
        "customer_can_view_transfer_history",
        "customer_can_export_transfer_history",
        "customer_can_search_transfer",
        "customer_can_repeat_transfer",
        "customer_can_cancel_transfer",
    ],
    "loans": [
        "customer_can_view_loan_schedule",
        "customer_can_make_loan_payment",
        "customer_can_download_loan_statement",
        "customer_can_view_interest_rate",
        "customer_can_request_early_repayment",
        "customer_can_view_remaining_balance",
        "customer_can_view_next_payment_date",
        "customer_can_download_amortization_table",
        "customer_can_request_loan_certificate",
        "customer_can_view_loan_history",
    ],
    "notifications": [
        "customer_receives_sms_notification",
        "customer_receives_email_notification",
        "customer_receives_push_notification",
        "customer_can_manage_notification_preferences",
        "customer_can_disable_marketing_messages",
        "customer_can_enable_security_alerts",
        "customer_can_disable_security_alerts",
        "customer_can_view_notification_history",
        "customer_can_mark_notification_as_read",
        "customer_can_delete_notification",
    ],
    "security": [
        "customer_can_enable_two_factor_authentication",
        "customer_can_disable_two_factor_authentication",
        "customer_can_reset_password",
        "customer_can_change_password",
        "customer_can_change_security_question",
        "customer_can_view_login_history",
        "customer_session_expires_after_timeout",
        "customer_can_logout_from_all_devices",
        "customer_can_register_trusted_device",
        "customer_can_remove_trusted_device",
    ],
    "reports": [
        "customer_can_generate_monthly_report",
        "customer_can_generate_yearly_report",
        "customer_can_export_report_pdf",
        "customer_can_export_report_xlsx",
        "customer_can_filter_report_by_period",
        "customer_can_filter_report_by_account",
        "customer_can_download_tax_report",
        "customer_can_generate_spending_report",
        "customer_can_generate_income_report",
        "customer_can_schedule_report",
    ],
    "investments": [
        "customer_can_view_portfolio",
        "customer_can_buy_asset",
        "customer_can_sell_asset",
        "customer_can_view_asset_price",
        "customer_can_view_portfolio_performance",
        "customer_can_view_dividend_history",
        "customer_can_download_portfolio_report",
        "customer_can_filter_assets",
        "customer_can_search_asset",
        "customer_can_view_asset_details",
    ],
    "support": [
        "customer_can_create_support_ticket",
        "customer_can_view_ticket_status",
        "customer_can_add_ticket_comment",
        "customer_can_close_ticket",
        "customer_can_reopen_ticket",
        "customer_can_upload_attachment",
        "customer_can_download_attachment",
        "customer_can_rate_support_request",
        "customer_can_view_support_history",
        "customer_can_contact_support",
    ],
}

TOTAL_TESTS = 1000
FAILED_TESTS = 40
FLAKY_TESTS = 10

lines = [
    "import os",
    "import time",
    "import pytest",
    "import allure",
    "",
    'RUN_NUMBER = int(os.getenv("RUN_NUMBER", "1"))',
    "",
]

all_scenarios = []

for feature, scenarios in FEATURES.items():
    for scenario in scenarios:
        all_scenarios.append((feature, scenario))

for index in range(TOTAL_TESTS):
    case_id = 10001 + index

    feature, scenario = all_scenarios[index % len(all_scenarios)]

    title = scenario.replace("_", " ").capitalize()

    # Средняя длительность ~3.6 сек
    if feature in ("accounts", "cards"):
        sleep_time = 1

    elif feature in ("payments", "transfers", "loans"):
        sleep_time = 3

    else:
        sleep_time = 5

    lines.extend(
        [
            f'@allure.feature("{feature.title()}")',
            f'@allure.title("{title}")',
            f"def test_{scenario}_{case_id}():",
            "    with allure.step('Prepare test data'):",
            f'        allure.attach("{case_id}", "Case ID", allure.attachment_type.TEXT)',
            "",
            "    with allure.step('Execute business operation'):",
            f"        time.sleep({sleep_time})",
            "",
        ]
    )

    if index < FAILED_TESTS:
        lines.extend(
            [
                "    with allure.step('Validate business rule'):",
                '        pytest.fail("Known defect in business logic")',
            ]
        )

    elif index < FAILED_TESTS + FLAKY_TESTS:
        lines.extend(
            [
                "    with allure.step('Call external dependency'):",
                "        if RUN_NUMBER % 2 == 0:",
                '            pytest.fail("Intermittent timeout in external service")',
            ]
        )

    else:
        lines.extend(
            [
                "    with allure.step('Validate result'):",
                "        assert True",
            ]
        )

    lines.append("")
    lines.append("")

Path("test_banking_demo.py").write_text(
    "\n".join(lines),
    encoding="utf-8",
)

print("Generated 1000 test cases")
print("Expected duration: ~60 minutes")
print("950 PASS / 40 FAIL / 10 FLAKY")