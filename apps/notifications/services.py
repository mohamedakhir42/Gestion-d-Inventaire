"""
Email service using Resend.
"""

import logging
from typing import Any, Dict, List

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import translation

logger = logging.getLogger(__name__)


class EmailService:
    """Abstract email service for sending emails."""

    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: str = None,
        from_email: str = None,
        cc: List[str] = None,
        bcc: List[str] = None,
    ) -> bool:
        """Send an email."""
        try:
            from_email = from_email or settings.DEFAULT_FROM_EMAIL

            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content or html_content,
                from_email=from_email,
                to=[to_email],
                cc=cc or [],
                bcc=bcc or [],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            logger.info(f"Email sent successfully to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False


class TemplateEmailService(EmailService):
    """Service for sending templated emails."""

    def send_templated_email(
        self,
        to_email: str,
        template_name: str,
        context: Dict[str, Any],
        subject: str = None,
        from_email: str = None,
        language: str = None,
    ) -> bool:
        """Send a templated email."""
        try:
            if language:
                translation.activate(language)

            html_content = render_to_string(f"emails/{template_name}.html", context)
            text_content = render_to_string(f"emails/{template_name}.txt", context)

            if not subject:
                subject = context.get("subject", "Notification")

            return self.send_email(
                to_email=to_email,
                subject=subject,
                html_content=html_content,
                text_content=text_content,
                from_email=from_email,
            )
        except Exception as e:
            logger.error(f"Failed to send templated email to {to_email}: {str(e)}")
            return False
        finally:
            if language:
                translation.deactivate()


class InvitationEmailService(TemplateEmailService):
    """Service for sending invitation emails."""

    def send_invitation_email(
        self,
        to_email: str,
        invitation_token: str,
        inviter_name: str,
        company_name: str = None,
    ) -> bool:
        """Send invitation email to new user."""
        context = {
            "to_email": to_email,
            "invitation_token": invitation_token,
            "inviter_name": inviter_name,
            "company_name": company_name or "Our Company",
            "subject": "You're invited to join our Inventory Management System",
        }

        return self.send_templated_email(
            to_email=to_email,
            template_name="invitation",
            context=context,
        )


class PasswordResetEmailService(TemplateEmailService):
    """Service for sending password reset emails."""

    def send_password_reset_email(
        self,
        to_email: str,
        reset_token: str,
        user_name: str,
    ) -> bool:
        """Send password reset email."""
        context = {
            "to_email": to_email,
            "reset_token": reset_token,
            "user_name": user_name,
            "subject": "Password Reset Request",
        }

        return self.send_templated_email(
            to_email=to_email,
            template_name="password_reset",
            context=context,
        )


class LowStockEmailService(TemplateEmailService):
    """Service for sending low stock alert emails."""

    def send_low_stock_alert(
        self,
        to_email: str,
        products: List[Dict[str, Any]],
        warehouse_name: str,
    ) -> bool:
        """Send low stock alert email."""
        context = {
            "to_email": to_email,
            "products": products,
            "warehouse_name": warehouse_name,
            "subject": f"Low Stock Alert - {warehouse_name}",
        }

        return self.send_templated_email(
            to_email=to_email,
            template_name="low_stock_alert",
            context=context,
        )


class StockRequestEmailService(TemplateEmailService):
    """Service for sending stock request notification emails."""

    def send_request_approved_email(
        self,
        to_email: str,
        request_reference: str,
        approver_name: str,
    ) -> bool:
        """Send request approved email."""
        context = {
            "to_email": to_email,
            "request_reference": request_reference,
            "approver_name": approver_name,
            "subject": f"Stock Request Approved - {request_reference}",
        }

        return self.send_templated_email(
            to_email=to_email,
            template_name="request_approved",
            context=context,
        )

    def send_request_rejected_email(
        self,
        to_email: str,
        request_reference: str,
        rejecter_name: str,
        rejection_reason: str,
    ) -> bool:
        """Send request rejected email."""
        context = {
            "to_email": to_email,
            "request_reference": request_reference,
            "rejecter_name": rejecter_name,
            "rejection_reason": rejection_reason,
            "subject": f"Stock Request Rejected - {request_reference}",
        }

        return self.send_templated_email(
            to_email=to_email,
            template_name="request_rejected",
            context=context,
        )


class NotificationService:
    """Main notification service that delegates to specific services."""

    def __init__(self):
        """Initialize notification service."""
        self.invitation_service = InvitationEmailService()
        self.password_reset_service = PasswordResetEmailService()
        self.low_stock_service = LowStockEmailService()
        self.stock_request_service = StockRequestEmailService()

    def send_invitation(
        self,
        to_email: str,
        invitation_token: str,
        inviter_name: str,
        company_name: str = None,
    ) -> bool:
        """Send invitation email."""
        return self.invitation_service.send_invitation_email(
            to_email=to_email,
            invitation_token=invitation_token,
            inviter_name=inviter_name,
            company_name=company_name,
        )

    def send_password_reset(
        self,
        to_email: str,
        reset_token: str,
        user_name: str,
    ) -> bool:
        """Send password reset email."""
        return self.password_reset_service.send_password_reset_email(
            to_email=to_email,
            reset_token=reset_token,
            user_name=user_name,
        )

    def send_low_stock_alert(
        self,
        to_email: str,
        products: List[Dict[str, Any]],
        warehouse_name: str,
    ) -> bool:
        """Send low stock alert."""
        return self.low_stock_service.send_low_stock_alert(
            to_email=to_email,
            products=products,
            warehouse_name=warehouse_name,
        )

    def send_request_approved(
        self,
        to_email: str,
        request_reference: str,
        approver_name: str,
    ) -> bool:
        """Send request approved notification."""
        return self.stock_request_service.send_request_approved_email(
            to_email=to_email,
            request_reference=request_reference,
            approver_name=approver_name,
        )

    def send_request_rejected(
        self,
        to_email: str,
        request_reference: str,
        rejecter_name: str,
        rejection_reason: str,
    ) -> bool:
        """Send request rejected notification."""
        return self.stock_request_service.send_request_rejected_email(
            to_email=to_email,
            request_reference=request_reference,
            rejecter_name=rejecter_name,
            rejection_reason=rejection_reason,
        )
