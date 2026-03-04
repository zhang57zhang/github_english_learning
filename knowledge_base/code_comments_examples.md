# GitHub场景知识库 - 代码注释范例

## 1. 函数说明注释（Function Documentation）

### 1.1 标准Docstring格式

```python
def calculate_average(numbers: list[float]) -> float:
    """
    Calculate the arithmetic mean of a list of numbers.
    
    This function computes the average of all numbers in the input list.
    It handles edge cases such as empty lists and validates input types.
    
    Args:
        numbers: A list of numeric values to calculate the average from.
                 Must contain at least one element.
    
    Returns:
        The arithmetic mean of the input numbers as a float.
    
    Raises:
        ValueError: If the input list is empty.
        TypeError: If any element in the list is not a number.
    
    Example:
        >>> calculate_average([1, 2, 3, 4, 5])
        3.0
        >>> calculate_average([10.5, 20.5])
        15.5
    
    Note:
        This function uses floating-point arithmetic and may have
        precision issues with very large or very small numbers.
    
    See Also:
        calculate_median: Calculate the median of a list
        calculate_std_dev: Calculate standard deviation
    """
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    
    total = sum(numbers)
    return total / len(numbers)
```

**学习要点：**
- **Calculate the arithmetic mean**: 计算算术平均值
- **arithmetic mean**: 算术平均值
- **edge cases**: 边界情况
- **validates input types**: 验证输入类型
- **Args**: 参数
- **numeric values**: 数值
- **Returns**: 返回值
- **Raises**: 抛出异常
- **Example**: 示例
- **Note**: 注意事项
- **floating-point arithmetic**: 浮点运算
- **precision issues**: 精度问题
- **See Also**: 另见

### 1.2 复杂函数文档

```python
async def fetch_user_data(
    user_id: int,
    *,
    include_profile: bool = False,
    include_orders: bool = False,
    timeout: int = 30
) -> dict[str, Any]:
    """
    Fetch comprehensive user data from multiple sources asynchronously.
    
    This function retrieves user information from the database and optionally
    includes related data such as profile details and order history. All
    database queries are executed concurrently for optimal performance.
    
    Args:
        user_id: Unique identifier for the user. Must be a positive integer.
        include_profile: If True, fetches detailed profile information including
                        avatar, bio, and preferences. Default: False.
        include_orders: If True, fetches the user's order history for the past
                       30 days. Default: False.
        timeout: Maximum time in seconds to wait for all database queries to
                complete. If exceeded, a TimeoutError is raised. Default: 30.
    
    Returns:
        A dictionary containing user data with the following structure:
        {
            "id": int,              # User ID
            "username": str,        # Username
            "email": str,           # Email address
            "created_at": str,      # ISO 8601 timestamp
            "profile": dict | None, # Profile data (if requested)
            "orders": list | None   # Order history (if requested)
        }
    
    Raises:
        ValueError: If user_id is not positive.
        UserNotFoundError: If no user exists with the given ID.
        TimeoutError: If database queries exceed the timeout limit.
        DatabaseError: If there's an issue connecting to the database.
    
    Example:
        Basic usage:
        >>> user = await fetch_user_data(123)
        >>> print(user["username"])
        "john_doe"
        
        With optional data:
        >>> user = await fetch_user_data(
        ...     123,
        ...     include_profile=True,
        ...     include_orders=True
        ... )
        >>> print(user["profile"]["avatar"])
        "https://example.com/avatar.jpg"
    
    Performance:
        - Without optional data: ~50ms
        - With profile: ~80ms (concurrent)
        - With all options: ~120ms (concurrent)
    
    Warning:
        Enabling both include_profile and include_orders can significantly
        increase memory usage for users with extensive order history.
    
    Version Added:
        2.1.0
    
    Changed in Version:
        2.2.0: Added timeout parameter
        2.3.0: Now raises UserNotFoundError instead of returning None
    """
    if user_id <= 0:
        raise ValueError("user_id must be positive")
    
    # Implementation here
    ...
```

**学习要点：**
- **Fetch comprehensive user data**: 获取全面的用户数据
- **multiple sources**: 多个来源
- **asynchronously**: 异步地
- **related data**: 相关数据
- **order history**: 订单历史
- **executed concurrently**: 并发执行
- **optimal performance**: 最佳性能
- **Unique identifier**: 唯一标识符
- **positive integer**: 正整数
- **detailed profile information**: 详细个人信息
- **avatar, bio, and preferences**: 头像、简介和偏好
- **Maximum time**: 最长时间
- **exceeded**: 超过
- **structure**: 结构
- **ISO 8601 timestamp**: ISO 8601时间戳
- **optional data**: 可选数据
- **concurrent**: 并发的
- **significantly increase**: 显著增加
- **extensive**: 大量的
- **Version Added**: 版本添加
- **Changed in Version**: 版本变更

---

## 2. 算法解释注释（Algorithm Explanation）

### 2.1 排序算法注释

```python
def quicksort(arr: list[int]) -> list[int]:
    """
    Sort a list of integers using the quicksort algorithm.
    
    Time Complexity:
        - Best case: O(n log n)
        - Average case: O(n log n)
        - Worst case: O(n²) - when pivot is always smallest/largest
    
    Space Complexity:
        - O(log n) for recursion stack
    
    Algorithm Steps:
        1. Choose a pivot element (we use the last element)
        2. Partition: reorder array so elements < pivot come before,
           elements > pivot come after
        3. Recursively apply quicksort to sub-arrays
    
    Stability:
        Not stable - equal elements may be reordered
    
    Example:
        >>> quicksort([3, 6, 8, 10, 1, 2, 1])
        [1, 1, 2, 3, 6, 8, 10]
    """
    # Base case: arrays with 0 or 1 element are already sorted
    if len(arr) <= 1:
        return arr
    
    # Step 1: Choose pivot (last element)
    pivot = arr[-1]
    
    # Step 2: Partition array into three parts
    # - left: elements smaller than pivot
    # - middle: elements equal to pivot
    # - right: elements larger than pivot
    left = [x for x in arr[:-1] if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr[:-1] if x > pivot]
    
    # Step 3: Recursively sort and combine
    return quicksort(left) + middle + quicksort(right)
```

**学习要点：**
- **Time Complexity**: 时间复杂度
- **Best/Average/Worst case**: 最佳/平均/最坏情况
- **pivot**: 基准点
- **Space Complexity**: 空间复杂度
- **recursion stack**: 递归栈
- **Algorithm Steps**: 算法步骤
- **Partition**: 分区
- **reorder**: 重新排序
- **Recursively apply**: 递归应用
- **sub-arrays**: 子数组
- **Stability**: 稳定性
- **Not stable**: 不稳定
- **equal elements**: 相等元素
- **reordered**: 重新排序
- **Base case**: 基础情况
- **already sorted**: 已排序
- **Partition array**: 分区数组
- **smaller than**: 小于
- **larger than**: 大于
- **Recursively sort**: 递归排序
- **combine**: 组合

### 2.2 搜索算法注释

```python
def binary_search(arr: list[int], target: int) -> int | None:
    """
    Search for a target value in a sorted array using binary search.
    
    Binary search works by repeatedly dividing the search interval in half.
    This is much faster than linear search for large datasets.
    
    Prerequisites:
        - The input array MUST be sorted in ascending order
        - All elements must be comparable with the target
    
    Time Complexity:
        O(log n) - we eliminate half the elements each iteration
    
    Space Complexity:
        O(1) - iterative implementation uses constant space
    
    Algorithm:
        1. Initialize left and right pointers to array bounds
        2. While left <= right:
           a. Calculate middle index
           b. If arr[mid] == target, return index
           c. If arr[mid] < target, search right half
           d. If arr[mid] > target, search left half
        3. If loop exits, target not found
    
    Args:
        arr: Sorted list of integers (ascending order)
        target: Value to search for
    
    Returns:
        Index of target if found, None if not found
    
    Example:
        >>> binary_search([1, 3, 5, 7, 9, 11], 7)
        3
        >>> binary_search([1, 3, 5, 7, 9, 11], 6)
        None
    
    Warning:
        If the input array is not sorted, results are undefined.
        Use arr.sort() before calling this function.
    
    See Also:
        linear_search: Simpler but slower O(n) search
        bisect: Python's built-in binary search module
    """
    # Initialize search bounds
    left = 0
    right = len(arr) - 1
    
    # Continue searching while bounds haven't crossed
    while left <= right:
        # Calculate middle index (avoid overflow)
        mid = left + (right - left) // 2
        
        # Check if we found the target
        if arr[mid] == target:
            return mid
        
        # Target is in right half
        elif arr[mid] < target:
            left = mid + 1
        
        # Target is in left half
        else:
            right = mid - 1
    
    # Target not found
    return None
```

**学习要点：**
- **Search for a target value**: 搜索目标值
- **sorted array**: 排序数组
- **binary search**: 二分搜索
- **repeatedly dividing**: 重复划分
- **search interval**: 搜索区间
- **in half**: 一分为二
- **much faster**: 快得多
- **linear search**: 线性搜索
- **large datasets**: 大型数据集
- **Prerequisites**: 前提条件
- **sorted in ascending order**: 升序排序
- **comparable**: 可比较的
- **eliminate**: 消除
- **each iteration**: 每次迭代
- **iterative implementation**: 迭代实现
- **constant space**: 常数空间
- **Initialize**: 初始化
- **pointers**: 指针
- **array bounds**: 数组边界
- **Calculate middle index**: 计算中间索引
- **search right half**: 搜索右半部分
- **search left half**: 搜索左半部分
- **loop exits**: 循环退出
- **not found**: 未找到
- **ascending order**: 升序
- **Index of target**: 目标索引
- **undefined**: 未定义的
- **built-in**: 内置的

---

## 3. 业务逻辑注释（Business Logic）

### 3.1 支付处理逻辑

```python
def process_payment(
    order_id: str,
    payment_method: str,
    amount: float
) -> PaymentResult:
    """
    Process a payment for an order with comprehensive validation and error handling.
    
    Business Logic Flow:
        1. Validate order exists and is payable
        2. Validate payment method and amount
        3. Check fraud detection rules
        4. Process payment with payment gateway
        5. Update order status
        6. Send confirmation email
        7. Log transaction for audit
    
    Validation Rules:
        - Order must exist and have status "pending"
        - Amount must match order total (tolerance: $0.01)
        - Payment method must be active and supported
        - User must not be flagged for fraud
        - Daily transaction limit: $10,000
    
    Error Handling:
        - InvalidOrderError: Order doesn't exist or wrong status
        - PaymentValidationError: Amount or method validation failed
        - FraudDetectedError: Transaction flagged as potentially fraudulent
        - PaymentGatewayError: Communication with payment provider failed
    
    Args:
        order_id: Unique identifier for the order (format: ORD-XXXXX)
        payment_method: Payment method code (e.g., "credit_card", "paypal")
        amount: Payment amount in USD (must be positive)
    
    Returns:
        PaymentResult object containing:
        - success: bool
        - transaction_id: str | None
        - error_message: str | None
    
    Example:
        >>> result = process_payment("ORD-12345", "credit_card", 99.99)
        >>> if result.success:
        ...     print(f"Payment processed: {result.transaction_id}")
        ... else:
        ...     print(f"Payment failed: {result.error_message}")
    
    Security:
        - All payment data is encrypted at rest and in transit
        - PCI DSS compliant
        - Sensitive data is logged with masking
    
    Audit:
        - Transaction ID: TXN-XXXXX
        - Timestamp: ISO 8601 format
        - User ID, IP address, and user agent logged
    
    Performance:
        - Average processing time: 2-3 seconds
        - Timeout: 30 seconds
    
    Side Effects:
        - Updates order status in database
        - Sends email to customer
        - Creates audit log entry
        - May trigger fraud alert notification
    
    Note:
        This function is idempotent - processing the same payment twice
        will return the same result without charging twice.
    """
    # Step 1: Validate order
    order = get_order(order_id)
    if not order:
        raise InvalidOrderError(f"Order {order_id} not found")
    
    if order.status != "pending":
        raise InvalidOrderError(
            f"Order {order_id} has status '{order.status}', expected 'pending'"
        )
    
    # Step 2: Validate amount (allow $0.01 tolerance for floating-point)
    if abs(order.total - amount) > 0.01:
        raise PaymentValidationError(
            f"Amount {amount} doesn't match order total {order.total}"
        )
    
    # Step 3: Check fraud detection rules
    # Rule 1: Check if user is flagged
    if order.user.is_flagged:
        raise FraudDetectedError("User account is flagged for suspicious activity")
    
    # Rule 2: Check daily transaction limit
    daily_total = get_user_daily_total(order.user_id)
    if daily_total + amount > 10_000:
        raise FraudDetectedError(
            f"Daily transaction limit exceeded: ${daily_total + amount:,.2f} > $10,000"
        )
    
    # Rule 3: Check velocity (max 10 transactions per hour)
    hourly_count = get_user_hourly_transaction_count(order.user_id)
    if hourly_count >= 10:
        raise FraudDetectedError(
            f"Too many transactions: {hourly_count} in the last hour"
        )
    
    # Step 4: Process payment with gateway
    try:
        transaction = payment_gateway.charge(
            payment_method=payment_method,
            amount=amount,
            metadata={"order_id": order_id}
        )
    except PaymentGatewayError as e:
        # Log the error for debugging
        logger.error(f"Payment gateway error for order {order_id}: {e}")
        raise
    
    # Step 5: Update order status
    order.status = "paid"
    order.transaction_id = transaction.id
    order.paid_at = datetime.now()
    db.commit()
    
    # Step 6: Send confirmation email (async, don't wait)
    send_email_async(
        to=order.user.email,
        template="payment_confirmation",
        context={"order": order, "transaction": transaction}
    )
    
    # Step 7: Create audit log
    create_audit_log(
        action="payment_processed",
        user_id=order.user_id,
        details={
            "order_id": order_id,
            "transaction_id": transaction.id,
            "amount": amount,
            "payment_method": payment_method
        }
    )
    
    return PaymentResult(
        success=True,
        transaction_id=transaction.id,
        error_message=None
    )
```

**学习要点：**
- **comprehensive validation**: 全面验证
- **error handling**: 错误处理
- **Business Logic Flow**: 业务逻辑流程
- **Validate order exists**: 验证订单存在
- **payable**: 可支付的
- **Validate payment method**: 验证支付方式
- **Check fraud detection rules**: 检查欺诈检测规则
- **Process payment**: 处理支付
- **payment gateway**: 支付网关
- **Update order status**: 更新订单状态
- **Send confirmation email**: 发送确认邮件
- **Log transaction**: 记录交易
- **audit**: 审计
- **Validation Rules**: 验证规则
- **pending**: 待处理的
- **tolerance**: 容差
- **active and supported**: 激活且支持的
- **flagged for fraud**: 标记为欺诈
- **Daily transaction limit**: 每日交易限额
- **Error Handling**: 错误处理
- **InvalidOrderError**: 无效订单错误
- **PaymentValidationError**: 支付验证错误
- **FraudDetectedError**: 检测到欺诈错误
- **PaymentGatewayError**: 支付网关错误
- **Security**: 安全性
- **encrypted at rest and in transit**: 静态和传输中加密
- **PCI DSS compliant**: 符合PCI DSS标准
- **Sensitive data**: 敏感数据
- **masking**: 掩码
- **Timestamp**: 时间戳
- **user agent**: 用户代理
- **Performance**: 性能
- **processing time**: 处理时间
- **Timeout**: 超时
- **Side Effects**: 副作用
- **idempotent**: 幂等的
- **charging twice**: 收费两次
- **tolerance for floating-point**: 浮点容差
- **suspicious activity**: 可疑活动
- **exceeded**: 超过
- **velocity**: 速度/频率
- **metadata**: 元数据
- **async**: 异步
- **don't wait**: 不等待

### 3.2 用户权限检查

```python
def check_user_permission(
    user: User,
    resource: str,
    action: str
) -> bool:
    """
    Check if a user has permission to perform an action on a resource.
    
    Permission Hierarchy (from highest to lowest):
        1. Super Admin: Full access to everything
        2. Admin: Full access to their organization
        3. Manager: Read/write access to their team's resources
        4. Member: Read access to their team's resources
        5. Guest: Limited read access
    
    Permission Logic:
        - Check if user is super admin (bypass all checks)
        - Check if user's role has explicit permission
        - Check if permission is granted via access control list (ACL)
        - Check if action is allowed on resource type
        - Default: Deny access
    
    Args:
        user: User object containing role and permissions
        resource: Resource identifier (e.g., "project:123", "user:456")
        action: Action to perform (e.g., "read", "write", "delete")
    
    Returns:
        True if user has permission, False otherwise
    
    Example:
        >>> user = get_user(123)
        >>> has_permission = check_user_permission(user, "project:456", "write")
        >>> if has_permission:
        ...     update_project(456, data)
        ... else:
        ...     raise PermissionError("Access denied")
    
    Caching:
        Results are cached for 5 minutes per user/resource/action combination
        to reduce database queries. Cache is invalidated when user's role changes.
    
    Security:
        - Follows principle of least privilege
        - All permission checks are logged
        - Failed checks trigger security alert if suspicious pattern detected
    
    Performance:
        - With cache hit: ~1ms
        - With cache miss: ~10ms (includes database query)
    
    Note:
        This function should be called before any sensitive operation.
        Never rely solely on client-side permission checks.
    """
    # Check cache first
    cache_key = f"permission:{user.id}:{resource}:{action}"
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result
    
    # Rule 1: Super admin has full access
    if user.role == "super_admin":
        logger.info(f"Super admin {user.id} granted access to {resource}:{action}")
        return True
    
    # Rule 2: Check explicit role-based permission
    role_permission = f"{user.role}:{resource_type(resource)}:{action}"
    if role_permission in PERMISSION_MATRIX:
        has_access = PERMISSION_MATRIX[role_permission]
        cache.set(cache_key, has_access, ttl=300)
        return has_access
    
    # Rule 3: Check ACL (Access Control List)
    acl_entry = db.query(ACL).filter(
        ACL.user_id == user.id,
        ACL.resource == resource,
        ACL.action == action
    ).first()
    
    if acl_entry:
        cache.set(cache_key, acl_entry.allowed, ttl=300)
        return acl_entry.allowed
    
    # Rule 4: Check resource-specific permissions
    # (e.g., user can only edit their own profile)
    if resource.startswith("user:"):
        resource_user_id = int(resource.split(":")[1])
        if action == "write" and user.id == resource_user_id:
            cache.set(cache_key, True, ttl=300)
            return True
    
    # Default: Deny access
    logger.warning(
        f"Permission denied: user {user.id} cannot {action} on {resource}"
    )
    cache.set(cache_key, False, ttl=300)
    return False
```

**学习要点：**
- **Check if a user has permission**: 检查用户是否有权限
- **perform an action**: 执行操作
- **Permission Hierarchy**: 权限层级
- **from highest to lowest**: 从高到低
- **Super Admin**: 超级管理员
- **Full access**: 完全访问
- **bypass all checks**: 绕过所有检查
- **explicit permission**: 显式权限
- **access control list**: 访问控制列表
- **ACL**: 访问控制列表
- **resource type**: 资源类型
- **Default: Deny access**: 默认拒绝访问
- **Resource identifier**: 资源标识符
- **Caching**: 缓存
- **cache hit/miss**: 缓存命中/未命中
- - **reduce database queries**: 减少数据库查询
- **invalidated**: 失效
- **principle of least privilege**: 最小权限原则
- **permission checks**: 权限检查
- **security alert**: 安全警报
- **suspicious pattern**: 可疑模式
- **sensitive operation**: 敏感操作
- **client-side**: 客户端
- **role-based permission**: 基于角色的权限
- **PERMISSION_MATRIX**: 权限矩阵
- **resource-specific**: 资源特定的
- **edit their own profile**: 编辑自己的资料
- **Permission denied**: 权限被拒绝

---

## 4. 配置文件注释（Configuration Files）

### 4.1 YAML配置文件

```yaml
# Application Configuration
# This file contains all configuration settings for the application.
# Copy this to config.yml and update values as needed.

# Server Configuration
server:
  # Host address to bind the server (use 0.0.0.0 for all interfaces)
  host: 0.0.0.0
  
  # Port number (must be between 1024 and 65535)
  port: 8000
  
  # Number of worker processes (recommended: CPU cores * 2)
  workers: 4
  
  # Enable debug mode (DO NOT use in production)
  debug: false
  
  # Request timeout in seconds
  timeout: 30

# Database Configuration
database:
  # Database type (postgresql, mysql, sqlite)
  type: postgresql
  
  # Connection settings
  host: localhost
  port: 5432
  name: myapp_db
  
  # Credentials (use environment variables in production!)
  username: ${DB_USERNAME}  # Set in .env file
  password: ${DB_PASSWORD}  # Set in .env file
  
  # Connection pool settings
  pool:
    # Minimum number of connections
    min_size: 5
    
    # Maximum number of connections
    max_size: 20
    
    # Maximum time to wait for connection (seconds)
    timeout: 10
  
  # SSL configuration
  ssl:
    enabled: true
    cert_path: /path/to/cert.pem
    key_path: /path/to/key.pem

# Redis Cache Configuration
redis:
  host: localhost
  port: 6379
  db: 0
  password: ${REDIS_PASSWORD}
  
  # Default TTL for cached items (seconds)
  default_ttl: 3600
  
  # Maximum memory usage (e.g., 256mb, 1gb)
  max_memory: 256mb

# Logging Configuration
logging:
  # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
  level: INFO
  
  # Log format (Python logging format string)
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  
  # Log to file
  file:
    enabled: true
    path: /var/log/myapp/app.log
    max_size: 10MB     # Rotate when file exceeds this size
    backup_count: 5    # Keep this many rotated files
  
  # Log to console
  console:
    enabled: true
    colorize: true

# Security Configuration
security:
  # Secret key for session encryption (CHANGE IN PRODUCTION!)
  secret_key: ${SECRET_KEY}
  
  # JWT token settings
  jwt:
    algorithm: HS256
    expiry_hours: 24
  
  # CORS settings
  cors:
    allowed_origins:
      - https://example.com
      - https://app.example.com
    allowed_methods:
      - GET
      - POST
      - PUT
      - DELETE
    allowed_headers:
      - Content-Type
      - Authorization

# Feature Flags
features:
  # Enable user registration
  user_registration: true
  
  # Enable email notifications
  email_notifications: true
  
  # Enable experimental features
  experimental:
    new_dashboard: false
    ai_recommendations: false
```

**学习要点：**
- **Application Configuration**: 应用配置
- **configuration settings**: 配置设置
- **Copy this to**: 复制到
- **update values**: 更新值
- **Server Configuration**: 服务器配置
- **Host address**: 主机地址
- **bind the server**: 绑定服务器
- **all interfaces**: 所有接口
- **Port number**: 端口号
- **worker processes**: 工作进程
- **CPU cores**: CPU核心
- **Enable debug mode**: 启用调试模式
- **Request timeout**: 请求超时
- **Database Configuration**: 数据库配置
- **Connection settings**: 连接设置
- **Credentials**: 凭证
- **environment variables**: 环境变量
- **Connection pool**: 连接池
- **Minimum/Maximum number**: 最小/最大数量
- **SSL configuration**: SSL配置
- **Redis Cache Configuration**: Redis缓存配置
- **Default TTL**: 默认生存时间
- **Maximum memory usage**: 最大内存使用
- **Logging Configuration**: 日志配置
- **Log level**: 日志级别
- **Log format**: 日志格式
- **Log to file/console**: 日志到文件/控制台
- **Rotate**: 轮转
- **exceeds**: 超过
- **rotated files**: 轮转文件
- **colorize**: 彩色化
- **Security Configuration**: 安全配置
- **Secret key**: 密钥
- **session encryption**: 会话加密
- **JWT token settings**: JWT令牌设置
- **expiry hours**: 过期小时数
- **CORS settings**: CORS设置
- **allowed origins/methods/headers**: 允许的源/方法/头部
- **Feature Flags**: 功能标志
- **Enable user registration**: 启用用户注册
- **email notifications**: 邮件通知
- **experimental features**: 实验性功能

### 4.2 Python配置文件

```python
"""
Application Configuration Module

This module loads configuration from environment variables and provides
default values for development. In production, set environment variables
appropriately.

Environment Variables:
    - DATABASE_URL: Database connection string
    - SECRET_KEY: Secret key for encryption
    - DEBUG: Enable debug mode (true/false)
    - LOG_LEVEL: Logging level (DEBUG, INFO, WARNING, ERROR)
"""

import os
from pathlib import Path
from typing import List

# Base directory of the application
BASE_DIR = Path(__file__).parent.parent

# Debug mode - enable only in development
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Secret key for session encryption
# WARNING: Change this in production!
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "dev-secret-key-change-in-production-please!"
)

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{BASE_DIR}/data/dev.db"
)

# Database connection pool settings
DATABASE_POOL_SIZE = int(os.getenv("DATABASE_POOL_SIZE", "5"))
DATABASE_MAX_OVERFLOW = int(os.getenv("DATABASE_MAX_OVERFLOW", "10"))

# Redis configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

# Cache settings
CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_DEFAULT_TIMEOUT", "3600"))  # 1 hour
CACHE_KEY_PREFIX = os.getenv("CACHE_KEY_PREFIX", "myapp:")

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO" if not DEBUG else "DEBUG")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = BASE_DIR / "logs" / "app.log"

# Email configuration
SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", "noreply@example.com")

# CORS settings
CORS_ALLOWED_ORIGINS: List[str] = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:3000,http://localhost:8080"
    ).split(",")
]

# Security settings
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "false").lower() == "true"
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "31536000"))  # 1 year
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# Session settings
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"

# Rate limiting
RATELIMIT_ENABLED = os.getenv("RATELIMIT_ENABLED", "true").lower() == "true"
RATELIMIT_PER_MINUTE = int(os.getenv("RATELIMIT_PER_MINUTE", "60"))
RATELIMIT_STORAGE_URL = REDIS_URL

# File upload settings
MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", str(16 * 1024 * 1024)))  # 16MB
UPLOAD_FOLDER = BASE_DIR / "uploads"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

# Feature flags
FEATURE_USER_REGISTRATION = os.getenv(
    "FEATURE_USER_REGISTRATION",
    "true"
).lower() == "true"

FEATURE_EMAIL_NOTIFICATIONS = os.getenv(
    "FEATURE_EMAIL_NOTIFICATIONS",
    "true"
).lower() == "true"

# Validation
if not DEBUG and SECRET_KEY == "dev-secret-key-change-in-production-please!":
    raise ValueError(
        "SECRET_KEY must be changed in production! "
        "Set the SECRET_KEY environment variable."
    )
```

**学习要点：**
- **Configuration Module**: 配置模块
- **loads configuration from**: 从...加载配置
- **default values**: 默认值
- **development**: 开发环境
- **production**: 生产环境
- **set environment variables**: 设置环境变量
- **appropriately**: 适当地
- **Base directory**: 基础目录
- **Debug mode**: 调试模式
- **enable only in development**: 仅在开发中启用
- **Secret key**: 密钥
- **session encryption**: 会话加密
- **WARNING**: 警告
- **connection string**: 连接字符串
- **connection pool**: 连接池
- **Cache settings**: 缓存设置
- **key prefix**: 键前缀
- **Logging configuration**: 日志配置
- **Email configuration**: 邮件配置
- **CORS settings**: CORS设置
- **Security settings**: 安全设置
- **SSL redirect**: SSL重定向
- **HSTS**: HTTP严格传输安全
- **content type nosniff**: 内容类型嗅探
- **browser XSS filter**: 浏览器XSS过滤器
- **Session settings**: 会话设置
- **cookie secure/httpOnly**: Cookie安全/仅HTTP
- **same site**: 同站
- **Rate limiting**: 速率限制
- **per minute**: 每分钟
- **File upload settings**: 文件上传设置
- **max content length**: 最大内容长度
- **upload folder**: 上传文件夹
- **allowed extensions**: 允许的扩展名
- **Feature flags**: 功能标志
- **Validation**: 验证
- **must be changed**: 必须更改

---

## 总结

### 代码注释核心词汇

| 英文 | 中文 | 使用频率 |
|------|------|----------|
| Args | 参数 | ⭐⭐⭐⭐⭐ |
| Returns | 返回值 | ⭐⭐⭐⭐⭐ |
| Raises | 抛出异常 | ⭐⭐⭐⭐⭐ |
| Example | 示例 | ⭐⭐⭐⭐⭐ |
| Time Complexity | 时间复杂度 | ⭐⭐⭐⭐ |
| Space Complexity | 空间复杂度 | ⭐⭐⭐⭐ |
| Algorithm | 算法 | ⭐⭐⭐⭐⭐ |
| Validation | 验证 | ⭐⭐⭐⭐⭐ |
| Business Logic | 业务逻辑 | ⭐⭐⭐⭐ |
| Error Handling | 错误处理 | ⭐⭐⭐⭐⭐ |
| Security | 安全性 | ⭐⭐⭐⭐ |
| Performance | 性能 | ⭐⭐⭐⭐⭐ |
| Configuration | 配置 | ⭐⭐⭐⭐⭐ |
| Environment Variables | 环境变量 | ⭐⭐⭐⭐⭐ |
| Debug Mode | 调试模式 | ⭐⭐⭐⭐ |
| Connection Pool | 连接池 | ⭐⭐⭐⭐ |
| Logging | 日志 | ⭐⭐⭐⭐⭐ |
| Feature Flags | 功能标志 | ⭐⭐⭐ |
| Caching | 缓存 | ⭐⭐⭐⭐ |
| idempotent | 幂等的 | ⭐⭐⭐ |
| principle of least privilege | 最小权限原则 | ⭐⭐⭐ |
| backward compatible | 向后兼容 | ⭐⭐⭐ |
