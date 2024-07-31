from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel
from sqlmodel import SQLModel


VERSION = 1


class BaseEntity(SQLModel):
    _schema_version: int = VERSION
    id: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None


class LegalEntity(BaseEntity):
    name: str
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]


class Human(LegalEntity):
    pass


class Company(LegalEntity):
    documents: list[Document]
    products: list[Product]
    accounts: list[Account]
    members: list[LegalEntity]

    @property
    def bank_user_accounts(self) -> list[BankUserAccount]:
        return [
            account for account in self.accounts if isinstance(account, BankUserAccount)
        ]


class Document(BaseEntity):
    name: str
    type: str
    content: str


class Action(BaseEntity):
    name: str
    description: str


class DocumentSubmission(Action):
    document: Document
    submitted_by: LegalEntity


class Account(BaseEntity):
    username: str
    email: str
    auth_credential_secrets: list[AuthCredentialSecret]
    platform_id: str


class Platform(BaseEntity):
    name: str
    description: str
    logo_url: str
    web_url: str
    openapi_url: str
    # implement static methods for the platform api here
    # the platform instance is or has a client object


class AuthCredentialSecret(BaseEntity):
    pass


class PasswordCredentialSecret(AuthCredentialSecret):
    # uses account email
    password: str


class MFACredentialSecret(AuthCredentialSecret):
    mfa_secret: str


class OAuthCredentialSecret(AuthCredentialSecret):
    pass


class GoogleOAuthCredentialSecret(AuthCredentialSecret):
    google_account: Account


class AppleOAuthCredentialSecret(AuthCredentialSecret):
    apple_account: Account


class FacebookOAuthCredentialSecret(AuthCredentialSecret):
    facebook_account: Account


class TwitterOAuthCredentialSecret(AuthCredentialSecret):
    twitter_account: Account


class EmailMagicLinkCredentialSecret(AuthCredentialSecret):
    # uses account email
    pass


class BankUserAccount(Account):
    accounts: list[BankAccount]
    bank: Bank


class Bank(BaseEntity):
    name: str
    address: str


class BankAccount(BaseEntity):
    name: str
    address: str
    number: str
    routing_number: str
    bank_user_account_id: str


class CheckingAccount(BankAccount):
    cards: list[Card]


class Card(BaseEntity):
    name: str
    address: str
    number: str
    expiration_date: datetime
    cvv: str
    bank_account_id: str


class SavingsAccount(BankAccount):
    fdic_code: str
    fdic_sub_code: str
    fdic_sub_code_description: str


class Product(BaseEntity):
    name: str
    description: str
    price: float
    sku: str
    category: str
    product_type: str  # 'physical', 'digital', 'service'


class Service(Product):
    duration: int  # in minutes
    is_recurring: bool


class SaaSProduct(Product):
    subscription_tiers: list["SubscriptionTier"]
    features: list[str]


class SubscriptionTier(BaseEntity):
    name: str
    price: float
    billing_cycle: str  # 'monthly', 'yearly', etc.
    features: list[str]


class ProductCategory(BaseEntity):
    name: str
    description: str
    parent_category: Optional["ProductCategory"] = None


class Inventory(BaseEntity):
    product: Product
    quantity: int
    location: str


class Order(BaseEntity):
    customer: "Customer"
    order_date: datetime
    status: str
    total_amount: float
    items: list["OrderItem"]


class OrderItem(BaseEntity):
    order: Order
    product: Product
    quantity: int
    price: float


class Customer(Account):
    orders: list[Order]
    reviews: list["Review"]
    subscriptions: list["Subscription"]


class Review(BaseEntity):
    product: Product
    customer: Customer
    rating: int
    comment: str
    review_date: datetime


class Discount(BaseEntity):
    code: str
    description: str
    percentage: float
    start_date: datetime
    end_date: datetime
    applicable_products: list[Product]


class Subscription(BaseEntity):
    customer: Customer
    saas_product: SaaSProduct
    tier: SubscriptionTier
    start_date: datetime
    end_date: datetime
    status: str
    billing_frequency: str


class CustomerSupportCase(BaseEntity):
    customer: Customer
    product: Product
    issue_description: str
    status: str
    created_date: datetime
    resolved_date: Optional[datetime]


class Feedback(BaseEntity):
    customer: Customer
    product: Product
    feedback_type: str  # 'bug', 'feature request', 'general'
    description: str
    submitted_date: datetime
    status: str
