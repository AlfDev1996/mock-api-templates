# Mock API Templates

> **Ready-to-use mock API templates** for REST and SOAP testing — no code required.
> Copy, paste, and get a live mock endpoint in seconds with [MockHub](https://mockhub.ovh) — the free online mock API generator.

[![MockHub](https://img.shields.io/badge/Powered%20by-MockHub-0d6efd)](https://mockhub.ovh)
[![Templates](https://img.shields.io/badge/Templates-11-brightgreen)](#-all-templates)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
**Last updated: 2026-03-31** · [![Last updated](https://img.shields.io/github/last-commit/AlfDev1996/mock-api-templates)](https://github.com/AlfDev1996/mock-api-templates/commits/main)

---

## Why mock APIs?

When you're building a frontend app, writing integration tests, or demoing a product — waiting for a real backend wastes time. A **mock REST API** returns pre-defined responses instantly, so you can:

- 🚀 Develop frontend features before the backend is ready
- 🧪 Test error handling (401, 404, 429, 500) reliably
- 🔁 Run CI/CD pipelines without depending on external services
- 🎨 Demo a product to clients without live infrastructure
- 📐 Prototype API contracts before writing real code

This repository contains **JSON templates** for the most common API patterns, ready to import into [MockHub](https://mockhub.ovh) or any other mock server.

---

## ⚡ Quickstart — live mock endpoint in 60 seconds

1. Open [mockhub.ovh](https://mockhub.ovh/api-generator/generate_api.html) — free, no credit card
2. Click **New API**
3. Pick a template from this repo, copy the response body
4. Set method, path, status code → **Save**
5. Done — your endpoint is live at `https://mockhub.ovh/mock/{your_id}/{path}`

```bash
# Test immediately with curl
curl https://mockhub.ovh/mock/your_id/products
```

> 💡 MockHub also supports **OpenAPI / Swagger import** — paste your spec and all endpoints are created automatically.
> 👉 [mockhub.ovh/api-generator/openapi_to_mock.html](https://mockhub.ovh/api-generator/openapi_to_mock.html)

---

## 📁 All Templates

### 🛒 E-commerce

| Template | Endpoints | Description |
|----------|-----------|-------------|
| [ecommerce/products-api.json](ecommerce/products-api.json) | 6 | Product catalog: list, get, create, update, delete + 404 |
| [ecommerce/cart-api.json](ecommerce/cart-api.json) | 5 | Cart: view, add/remove items, apply coupon + error |
| [ecommerce/orders-api.json](ecommerce/orders-api.json) | 4 | Orders: place, track, list, refund |

### 🔐 Authentication

| Template | Endpoints | Description |
|----------|-----------|-------------|
| [auth/jwt-auth.json](auth/jwt-auth.json) | 8 | JWT: register, login, refresh, me + 401/409 |
| [auth/oauth2-mock.json](auth/oauth2-mock.json) | 5 | OAuth2: token, introspection, userinfo |

### 💳 Payments

| Template | Endpoints | Description |
|----------|-----------|-------------|
| [payments/stripe-like.json](payments/stripe-like.json) | 6 | Stripe-inspired: payment intent, confirm, refund |
| [payments/paypal-like.json](payments/paypal-like.json) | 4 | PayPal-inspired: create order, capture, refund |

### 📱 Social

| Template | Endpoints | Description |
|----------|-----------|-------------|
| [social/users-feed.json](social/users-feed.json) | 6 | Profiles, feed, posts, likes, follow |
| [social/notifications.json](social/notifications.json) | 4 | List, mark read, push token |

### 🏢 SOAP / Enterprise

| Template | Operations | Description |
|----------|------------|-------------|
| [soap/hello-service.json](soap/hello-service.json) | 2 | Hello service + fault scenario |
| [soap/payment-service.json](soap/payment-service.json) | 4 | ProcessPayment, GetStatus, Cancel |

> **SOAP mocks:** upload your WSDL at [mockhub.ovh/api-generator/generate_soap.html](https://mockhub.ovh/api-generator/generate_soap.html)

### 🏥 Healthcare

| Template | Endpoints | Description |
|----------|-----------|-------------|
| [healthcare/patient-records.json](healthcare/patient-records.json) | 5 | FHIR-inspired: patients, observations, appointments |

---

## 🔀 Dynamic Variables

Every template uses **MockHub dynamic variables** — placeholders replaced with random realistic data on each request. No more hardcoded `"id": 1` in your mocks.

```json
{
  "id": "{{uuid}}",
  "user": {
    "name": "{{name}}",
    "email": "{{email}}",
    "joined": "{{isodate}}"
  },
  "score": "{{float}}",
  "active": "{{boolean}}"
}
```

| Variable | Example |
|----------|---------|
| `{{uuid}}` | `550e8400-e29b-41d4-a716-446655440000` |
| `{{name}}` | `John Smith` |
| `{{firstname}}` / `{{lastname}}` | `John` / `Smith` |
| `{{email}}` | `user4872@example.com` |
| `{{phone}}` | `+1-555-0192` |
| `{{isodate}}` | `2025-01-15T10:30:00Z` |
| `{{timestamp}}` | `1736934600000` |
| `{{integer}}` | `4821` |
| `{{float}}` | `49.99` |
| `{{boolean}}` | `true` |
| `{{word}}` | `falcon` |
| `{{sentence}}` | `The quick brown fox jumps over the lazy dog.` |
| `{{city}}` / `{{country}}` | `Berlin` / `Germany` |
| `{{zipcode}}` | `10115` |
| `{{company}}` | `Acme Corp` |
| `{{jobtitle}}` | `Senior Engineer` |
| `{{url}}` | `https://example.com/path` |
| `{{ipv4}}` | `192.168.1.42` |
| `{{color}}` | `#a3f2c1` |
| `{{creditcard}}` | `4111111111111111` |
| `{{iban}}` | `DE89370400440532013000` |

📖 Full docs: [mockhub.ovh/api-generator/docs.html](https://mockhub.ovh/api-generator/docs.html)

---

## 📄 Template format

```json
{
  "name": "API name",
  "description": "What this API mocks",
  "import_to_mockhub": "https://mockhub.ovh/api-generator/generate_api.html",
  "endpoints": [
    {
      "name": "Endpoint description",
      "method": "GET",
      "path": "/resource/:id",
      "status_code": 200,
      "headers": { "Content-Type": "application/json" },
      "delay_ms": 0,
      "response": {}
    }
  ]
}
```

Each endpoint can have **multiple scenarios** (different status codes / responses) — use MockHub's [Scenarios feature](https://mockhub.ovh/api-generator/article/how-to-add-scenario.html) to switch between them in tests.

---

## MockHub vs alternatives

| Feature | MockHub | Postman Mock | Mockoon | WireMock |
|---------|---------|-------------|---------|----------|
| No install required | ✅ Online | ✅ Online | ❌ Desktop | ❌ JAR/Docker |
| Free tier | ✅ 5 APIs | ⚠️ Limited | ✅ Open source | ✅ Open source |
| Dynamic variables | ✅ 20+ | ❌ | ✅ | ⚠️ Limited |
| SOAP mock support | ✅ | ❌ | ❌ | ✅ |
| AI-generated responses | ✅ | ❌ | ❌ | ❌ |
| OpenAPI import | ✅ | ✅ | ✅ | ✅ |
| Error scenario switching | ✅ | ⚠️ | ✅ | ✅ |
| Shareable public URL | ✅ | ✅ | ❌ | ❌ |

---


## 🔄 More Templates

<!-- AUTO-GENERATED TEMPLATES -->
| [ecommerce/inventory-api.json](ecommerce/inventory-api.json) | 9 | Warehouses, stock levels, SKUs, suppliers, purchase orders, low-stock alerts |
| [cms/blog-cms-api.json](cms/blog-cms-api.json) | 12 | Complete blog and content management system API with posts, categories, tags, au |
| Template | Endpoints | Description |
|----------|-----------|-------------|
| [messaging/messaging-api.json](messaging/messaging-api.json) | 12 | Full-featured messaging API supporting chat messages, conversations, channels, d |

## Contributing

New template ideas are welcome!

1. Fork the repo
2. Add your JSON file in the right category folder
3. Follow the template format above
4. Include at least one error scenario (4xx or 5xx)
5. Open a pull request — we'll review and merge it

---

## License

MIT — use freely in any project, commercial or personal.

---

<p align="center">
  Built for developers who don't want to wait for a backend.<br/>
  <strong><a href="https://mockhub.ovh/api-generator/register.html">Create your free mock API on MockHub →</a></strong>
</p>
