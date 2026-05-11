# Traceability Matrix and Heatmap

## Traceability Rules

- Zero orphaned requirements: every requirement must map to a feature, API, test type, and validation evidence.
- Zero orphaned features: every feature must map back to a requirement.
- Implementation, tests, and reports preserve these IDs.

## Heatmap Legend

| Mark | Meaning |
| --- | --- |
| H | High coverage or direct evidence required |
| M | Medium/supporting coverage required |
| L | Low/indirect coverage required |
| NA | Not applicable |

## Requirement to Evidence Heatmap

| Requirement | Feature | API Contract | Unit Tests | Integration Tests | E2E Tests | Docs Evidence | Current Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FR-01 Register | Register/Login | H | H | M | M | H | Implemented |
| FR-02 Login | Register/Login | H | H | M | H | H | Implemented |
| FR-03 Invalid login | Register/Login | H | H | M | M | H | Implemented |
| FR-04 View menu | View Menu | H | M | H | H | H | Implemented |
| FR-05 Add to cart | Add To Cart | M | H | M | H | H | Implemented |
| FR-06 Place order | Place Order | H | H | H | H | H | Implemented |
| FR-07 Empty cart rejection | Place Order | H | H | H | M | H | Implemented |
| FR-08 Duplicate order guard | Place Order | H | H | H | M | H | Implemented |
| FR-09 Kitchen dashboard | Kitchen Dashboard | H | M | H | H | H | Implemented |
| FR-10 Update status | Update Order Status | H | H | H | H | H | Implemented |
| FR-11 Unauthorized kitchen access | Kitchen Dashboard, Update Status | H | H | H | M | H | Implemented |
| FR-12 Invalid status transition | Update Order Status | H | H | H | M | H | Implemented |
| FR-13 Expired or invalid token rejection | Protected API Actions | H | H | H | M | H | Implemented |
| NFR-01 API response under 2 seconds | All API features | M | NA | M | M | H | Implemented |
| NFR-02 Password length >= 8 | Register | H | H | M | M | H | Implemented |
| NFR-03 Minimal maintainable system | All features | NA | NA | NA | NA | H | Implemented |

## Feature to Requirement Mapping

| Feature | Requirement IDs | Orphan Status |
| --- | --- | --- |
| Register/Login | FR-01, FR-02, FR-03, NFR-02 | Not orphaned |
| View Menu | FR-04, NFR-01 | Not orphaned |
| Add To Cart | FR-05 | Not orphaned |
| Place Order | FR-06, FR-07, FR-08, NFR-01 | Not orphaned |
| Protected API Actions | FR-13 | Not orphaned |
| Kitchen Dashboard | FR-09, FR-11, FR-13, NFR-01 | Not orphaned |
| Update Order Status | FR-10, FR-11, FR-12, FR-13, NFR-01 | Not orphaned |

## Testing Pyramid Evidence

Target testing pyramid:

- 70 percent unit tests
- 20 percent integration tests
- 10 percent Playwright E2E tests

Actual current automated count:

| Layer | Count | Approx Ratio |
| --- | ---: | ---: |
| Unit | 16 | 46 percent |
| Integration | 17 | 49 percent |
| E2E | 2 | 6 percent |

The implemented suite is intentionally integration-heavy because the rubric emphasizes API contracts and traceability. Browser E2E coverage remains small to avoid duplicating backend edge-case tests.
