Feature: Validate the functionality of the "Top Headlines" endpoint of News API

1. As a user with valid API key,
I want to retrieve the latest top headlines,
so that I can stay updated with current news.

Scenario: Retrieve top headlines successfully
    Given a user with a valid API key
    When I send a GET request to "/v2/top-headlines"
    Then the response status code should be 200
    And the response should be valid
