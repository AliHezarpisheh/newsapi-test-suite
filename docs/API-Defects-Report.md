# API Defect Report

## Auth Reports

## Inquiry: Behavior When API Key Sent in Two Ways

**Description:**
When the API key is sent both as a query parameter and in the HTTP header, and one of them is valid while the other is invalid, the `apiKey` query parameter takes precedence.

**Notes:**
This is not documented as a defect but requires clarification from the team on whether this is the intended behavior.

**HTTP Request:**
- **Method:** GET
- **Endpoint:** `/v2/everything`
- **Headers:**
  ```json
  {
      "Authorization": "Bearer invalid_key"
  }
  ```
- **Query Parameters:**
  ```json
  {
      "apiKey": "valid_key",
      "q": "technology"
  }
  ```

**Expected Result:**
Documented and consistent behavior for precedence of API key validation.

**Actual Result:**
The query parameter `apiKey` takes precedence over the HTTP header.

## `/everything` Endpoint

## Defect 1: Inconsistencies in API Response for `pageSize` > 100

**Description:**
The API exhibits inconsistent behavior when requesting more than 100 objects per page using the `pageSize` parameter.

**HTTP Request:**
- **Method:** GET
- **Endpoint:** `/v2/everything`
- **Headers:**
  ```json
  {
      "Authorization": "Bearer <API_KEY>"
  }
  ```
- **Query Parameters:**
  ```json
  {
      "q": "bitcoin",
      "pageSize": 101
  }
  ```

**Expected Result:**
Consistent error handling for all values exceeding the allowed limit (e.g., a clear and specific error message for `pageSize` > 100).

**Actual Result:**
- For `pageSize` = 101: `400 Bad Request` with the message indicating pageSize is too large.
- For `pageSize` > 200: `426 Upgrade Required` with the message indicating Client should upgrade its plan.

**Notes:**
Clarification is needed on whether this behavior is plan-specific or an unintended inconsistency.

---

## Defect 2: Missing Status Parameters for Null or Empty `page`/`pageSize`

**Description:**
When `null`, `None`, or an empty string is passed to the `page` or `pageSize` parameters, the API response format is broken, and no `code` or `status` fields are returned.

**HTTP Request:**
- **Method:** GET
- **Endpoint:** `/v2/everything`
- **Headers:**
  ```json
  {
      "Authorization": "Bearer <API_KEY>"
  }
  ```
- **Query Parameters:**
  ```json
  {
      "q": "tesla",
      "pageSize": ""
  }
  ```

**Expected Result:**
A clear and specific error response containing `code` and `status` fields.

**Actual Result:**
API response format is broken, and no `code` or `status` fields are included in the error response. The response body is: {"message": "The request is invalid."}

---

## Defect 3: Invalid String Handling for `page`/`pageSize`

**Description:**
When a string without digits (e.g., "abc") is passed to the `page` or `pageSize` parameters, the API responds successfully instead of returning an error.

**HTTP Request:**
- **Method:** GET
- **Endpoint:** `/v2/everything`
- **Headers:**
  ```json
  {
      "Authorization": "Bearer <API_KEY>"
  }
  ```
- **Query Parameters:**
  ```json
  {
      "q": "technology",
      "page": "abc"
  }
  ```

**Expected Result:**
An error response indicating invalid parameter value.

**Actual Result:**
The API responds successfully, potentially leading to unexpected behavior.

---

## Defect 4: Negative `pageSize` Causes Server Error

**Description:**
When a negative value is passed to the `pageSize` parameter, the server breaks and returns a generic error message.

**HTTP Request:**
- **Method:** GET
- **Endpoint:** `/v2/everything`
- **Headers:**
  ```json
  {
      "Authorization": "Bearer <API_KEY>"
  }
  ```
- **Query Parameters:**
  ```json
  {
      "q": "technology",
      "pageSize": -100
  }
  ```

**Expected Result:**
An error response with a clear and specific message about invalid parameter value.

**Actual Result:**
```json
{
    "status": "error",
    "code": "unexpectedError",
    "message": "Something went wrong. Your request may be malformed - please check the params and try again."
}
```

**Notes:**
The server should validate and handle negative values appropriately.

---

## Defect 6: Incorrect Use of 400 Bad Request for Server Errors

**Description:**
The API returns `400 Bad Request` for server errors, which is inconsistent with REST API conventions. Server errors should typically use 5xx status codes.

**HTTP Request:**
- **Method:** GET
- **Endpoint:** `/v2/everything`
- **Headers:**
  ```json
  {
      "Authorization": "Bearer <API_KEY>"
  }
  ```
- **Query Parameters:**
  ```json
  {
      "q": "technology",
      "pageSize": -1
  }
  ```

**Expected Result:**
A `500 Internal Server Error` or other appropriate 5xx status code for server-side issues.

**Actual Result:**
`400 Bad Request` is returned for server errors.

---

## Defect 7: Negative `pageSize` Produces Successful Response

**Description:**
Passing a negative value (e.g., `-1`) to the `pageSize` parameter results in a successful response instead of being rejected as an invalid input.

**HTTP Request:**
- **Method:** GET
- **Endpoint:** `/v2/everything`
- **Headers:**
  ```json
  {
      "Authorization": "Bearer <API_KEY>"
  }
  ```
- **Query Parameters:**
  ```json
  {
      "q": "technology",
      "pageSize": -1
  }
  ```

**Expected Result:**
An error response indicating invalid parameter value.

**Actual Result:**
The API responds successfully with an empty result set.

---

## Documentation Issue: Incorrect Sources Index Description

**Description:**
The API documentation incorrectly describes the `sources` index. The provided information does not match the actual functionality.

**Notes:**
This is a documentation issue that needs to be addressed for clarity and consistency.

---

## Defect 8: Inadequate Error Code for Query Malformation

**Description:**
The error code `unexpectedError` is too generic and does not provide sufficient information about query malformation. Additionally, the API does not handle malformed queries containing words ending with `)` properly.

**HTTP Request:**
- **Method:** GET
- **Endpoint:** `/v2/everything`
- **Headers:**
  ```json
  {
      "Authorization": "Bearer <API_KEY>"
  }
  ```
- **Query Parameters:**
  ```json
  {
      "q": "crypto)"
  }
  ```

**Expected Result:**
A descriptive error code such as `queryMalformed` and proper handling of malformed queries.

**Actual Result:**
`unexpectedError` is returned, and the malformed query is not handled correctly.

---

## Defect 9 (Critical): Empty JSON in `q` Parameter Returns Excessive Data

**Description:**
Passing an empty JSON object (e.g., `{}`) as a value for the `q` parameter results in a large number of articles being returned (1,860,197). This behavior suggests that the case is not handled properly by the back-end.

**HTTP Request:**
- **Method:** GET
- **Endpoint:** `/v2/everything`
- **Headers:**
  ```json
  {
      "Authorization": "Bearer <API_KEY>"
  }
  ```
- **Query Parameters:**
  ```json
  {
      "q": "{}"
  }
  ```

**Expected Result:**
An error response with the `missingParameter` code, similar to other cases where a nullable value is passed.

**Actual Result:**
A successful response with an excessive number of articles is returned.

## Defect 10: Timeout Error for Non-Existent `exclude_domains` Value

**Description:**
Setting a non-existent but valid domain format for the `exclude_domains` parameter frequently results in a timeout error, suggesting performance issues with handling this case.

**HTTP Request:**
- **Method:** GET
- **Endpoint:** `/v2/everything`
- **Headers:**
  ```json
  {
      "Authorization": "Bearer <API_KEY>"
  }
  ```
- **Query Parameters:**
  ```json
  {
      "q": "technology",
      "exclude_domains": "nonexistent.example.com"
  }
  ```

**Expected Result:**
A quick and clear response indicating no results found.

**Actual Result:**
The request times out in most cases, indicating potential performance concerns.

---

## Observation: Inconsistencies in Handling Invalid Parameters

**Description:**
The API exhibits inconsistent behavior when invalid parameters are passed. For example:
- An error is raised when an invalid value is passed to the `searchIn` parameter.
- No error is raised when `exclude_domains` receives an invalid value.

**Notes:**
This is not a defect but should be documented to ensure clarity and consistency in API behavior.

---

## Defect 11 (Critical): Incorrect Handling of `to` and `from` Parameters

**Description:**
Passing a `to` parameter earlier than the `from` parameter results in a successful response with a non-empty list of articles. This behavior is incorrect as it contradicts logical query expectations.

**HTTP Request:**
- **Method:** GET
- **Endpoint:** `/v2/everything`
- **Headers:**
  ```json
  {
      "Authorization": "Bearer <API_KEY>"
  }
  ```
- **Query Parameters:**
  ```json
  {
      "q": "technology",
      "to": "2025-01-01T10:00:00",
      "from": "2025-02-01T10:00:00"
  }
  ```

**Expected Result:**
An error response indicating invalid date range or no results.

**Actual Result:**
A successful response with a non-empty list of articles is returned.

---

## `/top-headlines/sources` Endpoint

## Observation: Inconsistent Behavior for Invalid Arguments in Sources Endpoint

**Description:**
When invalid arguments are provided for the `country`, `language`, or `category` parameters in the `/v2/sources` endpoint, the API exhibits inconsistent behavior:
- Some invalid arguments do not affect the response.
- Others result in an empty list of sources.

**HTTP Request:**
- **Method:** GET
- **Endpoint:** `/v2/sources`
- **Headers:**
  ```json
  {
      "Authorization": "Bearer <API_KEY>"
  }
  ```
- **Query Parameters:**
  ```json
  {
      "country": "invalid",
      "language": "invalid",
      "category": "invalid"
  }
  ```

**Expected Result:**
Consistent error handling for invalid arguments.

**Actual Result:**
The response behavior varies depending on the parameter.
