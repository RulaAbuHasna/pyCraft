# PyCraft Paginator

## Mission
PyCraft Paginator is a Python package designed to provide efficient pagination solutions for various data structures. With the increasing amount of data in modern applications, navigating large datasets can become inefficient and slow. This package addresses that problem by offering flexible and customizable pagination methods, making it easier to handle large amounts of data while maintaining optimal performance.

The name PyCraft was chosen because we plan to expand this package to include additional utilities and tools for developers, building a collection of helpful functionalities (or "crafts") that can be used to improve the development process across various scenarios.

## Problem
When working with large datasets, rendering all the data at once in the front-end can result in poor performance, especially for web applications. This can be due to:

- Excessive memory consumption: Handling large datasets all at once can cause memory bottlenecks.
- Slow response times: Fetching too much data at once leads to slower response times, affecting the user experience.
- UI overload: Presenting too many data items in a user interface can lead to rendering delays and poor performance in the browser.

One common solution to this problem is pagination, but traditional pagination (such as using offset-based queries in databases) may not be sufficient for all use cases, especially when dealing with large or dynamically changing datasets.

## Pagination Solutions
PyCraft Paginator offers two types of pagination to overcome these challenges:

### 1. Fake Pagination (Array Pagination)
Fake pagination involves dividing a large dataset into smaller chunks without relying on the database to paginate the data. This is especially useful when the data is already available in memory (e.g., in an array or a dictionary).

- **How it works**: Fake pagination simply slices the dataset into chunks based on predefined parameters (e.g., first, after, last, before), without actually changing the data's order.
- **When to use it**: Fake pagination is ideal for use cases where the dataset is already loaded in memory, and you want to display a subset of it at a time (e.g., paginating a list of items in the browser).

Example:
An array-based paginator slices the dataset into manageable chunks, where the first parameter specifies the number of items to show on the current page, and the after parameter specifies where the next page should start.

```python
data = [1, 2, 3, 4, 5]
paginator = ArrayPaginator(data, first=2)
print(paginator.page)
```
Output:
```
[1, 2]
```

### 2. Cursor-Based Pagination (DictPaginator)
Cursor-based pagination is an alternative that uses cursors to determine the current position in the dataset and retrieve the next set of items. This method is more efficient for handling large datasets as it avoids the performance overhead of offset-based queries.

- **How it works**: Cursor-based pagination encodes the position of the current item in a cursor, which is then passed to the API to fetch the next set of data. This is particularly useful when you want to paginate through a dictionary.
- **When to use it**: This type of pagination is ideal when you're working with large datasets, or when using databases or APIs that support cursor-based navigation.

Example:
A dictionary-based paginator uses a cursor to track the current position in a dataset and generate the next page of results based on that position.

```python
data = {"a": 1, "b": 2, "c": 3}
paginator = DictPaginator(data, first=2)
print(paginator.page)
```
Output:
```
{"a": 1, "b": 2}
```
## Solutions Provided

PyCraft Paginator helps solve the following common pagination problems:

### Efficient Pagination for Large Datasets
By using cursor-based pagination or fake pagination, PyCraft helps you efficiently navigate through large datasets without overloading memory or impacting performance.

### Flexible Pagination
The package allows for flexible pagination options such as first, last, after, and before parameters, making it adaptable to various use cases and data structures.

### Support for Custom Encoding
PyCraft provides the ability to use custom cursor encoders for advanced use cases, such as when you need to encode and decode positions for security reasons.

### Improved User Experience
With pagination, users can fetch only the data they need, which leads to faster load times and a smoother user experience in web applications.

# Further Reading

For more information about fake pagination, check out this Medium article:
[What Do You Mean Fake Pagination?](https://medium.com/@rula.abuhasna/what-do-you-mean-fake-pagination-b1ff5cd21918)
