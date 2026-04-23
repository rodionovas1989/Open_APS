"""
Модели данных для системы APS (Advanced Planning and Scheduling)

Этот модуль содержит все метаданные, с которыми работает система:
- Предприятия и рабочие центры
- Продукты и спецификации
- Ресурсы и их возможности
- Заказы и операции
- Планы и расписания
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
import enum

from src.database.connection import Base


# ==================== ENUMS ====================

class OrderStatus(enum.Enum):
    """Статусы заказа"""
    PENDING = "pending"  # Ожидает
    PLANNED = "planned"  # Запланирован
    IN_PROGRESS = "in_progress"  # В работе
    COMPLETED = "completed"  # Завершен
    CANCELLED = "cancelled"  # Отменен


class OperationStatus(enum.Enum):
    """Статусы операции"""
    NOT_STARTED = "not_started"  # Не начата
    READY = "ready"  # Готова к выполнению
    IN_PROGRESS = "in_progress"  # Выполняется
    PAUSED = "paused"  # Приостановлена
    COMPLETED = "completed"  # Завершена
    BLOCKED = "blocked"  # Заблокирована


class ResourceType(enum.Enum):
    """Типы ресурсов"""
    MACHINE = "machine"  # Оборудование
    LABOR = "labor"  # Персонал
    TOOL = "tool"  # Инструмент
    MATERIAL = "material"  # Материал
    SPACE = "space"  # Площадь/пространство


# ==================== BASE MODELS ====================

class TimestampMixin:
    """Миксин для добавления временных меток"""
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


# ==================== ENTERPRISE MODELS ====================

class Enterprise(Base, TimestampMixin):
    """Предприятие/Компания"""
    __tablename__ = "enterprises"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    code = Column(String(50), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    address = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Связи
    work_centers = relationship("WorkCenter", back_populates="enterprise", cascade="all, delete-orphan")
    warehouses = relationship("Warehouse", back_populates="enterprise", cascade="all, delete-orphan")


class WorkCenter(Base, TimestampMixin):
    """Рабочий центр - производственная единица"""
    __tablename__ = "work_centers"
    
    id = Column(Integer, primary_key=True, index=True)
    enterprise_id = Column(Integer, ForeignKey("enterprises.id"), nullable=False)
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    capacity_hours_per_day = Column(Float, default=8.0, nullable=False)  # Мощность в часах в день
    efficiency_factor = Column(Float, default=1.0, nullable=False)  # Коэффициент эффективности
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Связи
    enterprise = relationship("Enterprise", back_populates="work_centers")
    resources = relationship("Resource", back_populates="work_center", cascade="all, delete-orphan")
    operations = relationship("Operation", back_populates="work_center")
    
    __table_args__ = (
        Index("idx_work_centers_enterprise", "enterprise_id"),
    )


# ==================== RESOURCE MODELS ====================

class Resource(Base, TimestampMixin):
    """Ресурс - оборудование, персонал, инструмент"""
    __tablename__ = "resources"
    
    id = Column(Integer, primary_key=True, index=True)
    work_center_id = Column(Integer, ForeignKey("work_centers.id"), nullable=False)
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False)
    resource_type = Column(SQLEnum(ResourceType), nullable=False)
    capacity = Column(Float, default=1.0, nullable=False)  # Емкость ресурса
    efficiency = Column(Float, default=1.0, nullable=False)  # Эффективность
    cost_per_hour = Column(Float, default=0.0, nullable=False)  # Стоимость часа работы
    calendar_id = Column(Integer, ForeignKey("calendars.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Связи
    work_center = relationship("WorkCenter", back_populates="resources")
    calendar = relationship("Calendar", back_populates="resources")
    operation_resources = relationship("OperationResource", back_populates="resource")
    
    __table_args__ = (
        Index("idx_resources_work_center", "work_center_id"),
        Index("idx_resources_type", "resource_type"),
    )


class Calendar(Base, TimestampMixin):
    """Производственный календарь"""
    __tablename__ = "calendars"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Связи
    resources = relationship("Resource", back_populates="calendar")
    exceptions = relationship("CalendarException", back_populates="calendar", cascade="all, delete-orphan")
    working_periods = relationship("WorkingPeriod", back_populates="calendar", cascade="all, delete-orphan")


class CalendarException(Base, TimestampMixin):
    """Исключения из календаря (праздники, простои)"""
    __tablename__ = "calendar_exceptions"
    
    id = Column(Integer, primary_key=True, index=True)
    calendar_id = Column(Integer, ForeignKey("calendars.id"), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    exception_type = Column(String(50), nullable=False)  # holiday, maintenance, shutdown
    description = Column(String(500), nullable=True)
    
    # Связи
    calendar = relationship("Calendar", back_populates="exceptions")


class WorkingPeriod(Base, TimestampMixin):
    """Периоды работы в календаре"""
    __tablename__ = "working_periods"
    
    id = Column(Integer, primary_key=True, index=True)
    calendar_id = Column(Integer, ForeignKey("calendars.id"), nullable=False)
    day_of_week = Column(Integer, nullable=False)  # 0=Monday, 6=Sunday
    start_time = Column(String(8), nullable=False)  # HH:MM
    end_time = Column(String(8), nullable=False)  # HH:MM
    is_working = Column(Boolean, default=True, nullable=False)
    
    # Связи
    calendar = relationship("Calendar", back_populates="working_periods")


# ==================== PRODUCT MODELS ====================

class Product(Base, TimestampMixin):
    """Продукт/Изделие"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    unit_of_measure = Column(String(50), default="шт", nullable=False)  # Единица измерения
    weight = Column(Float, nullable=True)  # Вес
    dimensions = Column(String(100), nullable=True)  # Габариты
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Связи
    bill_of_materials = relationship("BillOfMaterials", back_populates="product", cascade="all, delete-orphan")
    routing = relationship("Routing", back_populates="product", cascade="all, delete-orphan")
    order_items = relationship("OrderItem", back_populates="product")
    
    __table_args__ = (
        Index("idx_products_code", "code"),
    )


class BillOfMaterials(Base, TimestampMixin):
    """Спецификация изделия (BOM)"""
    __tablename__ = "bill_of_materials"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    component_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    unit_of_measure = Column(String(50), default="шт", nullable=False)
    scrap_rate = Column(Float, default=0.0, nullable=False)  # Процент брака
    
    # Связи
    product = relationship("Product", foreign_keys=[product_id], back_populates="bill_of_materials")
    component = relationship("Product", foreign_keys=[component_id])
    
    __table_args__ = (
        Index("idx_bom_product", "product_id"),
        Index("idx_bom_component", "component_id"),
    )


class Routing(Base, TimestampMixin):
    """Маршрутная карта - последовательность операций"""
    __tablename__ = "routings"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    version = Column(String(20), default="1.0", nullable=False)
    description = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Связи
    product = relationship("Product", back_populates="routing")
    routing_operations = relationship("RoutingOperation", back_populates="routing", cascade="all, delete-orphan", order_by="RoutingOperation.sequence")
    
    __table_args__ = (
        Index("idx_routing_product", "product_id"),
    )


class RoutingOperation(Base, TimestampMixin):
    """Операция в маршрутной карте"""
    __tablename__ = "routing_operations"
    
    id = Column(Integer, primary_key=True, index=True)
    routing_id = Column(Integer, ForeignKey("routings.id"), nullable=False)
    sequence = Column(Integer, nullable=False)  # Порядок выполнения
    work_center_id = Column(Integer, ForeignKey("work_centers.id"), nullable=False)
    operation_name = Column(String(255), nullable=False)
    setup_time = Column(Float, default=0.0, nullable=False)  # Время наладки (часы)
    run_time_per_unit = Column(Float, default=0.0, nullable=False)  # Время на единицу (часы)
    queue_time = Column(Float, default=0.0, nullable=False)  # Время ожидания (часы)
    move_time = Column(Float, default=0.0, nullable=False)  # Время перемещения (часы)
    
    # Связи
    routing = relationship("Routing", back_populates="routing_operations")
    work_center = relationship("WorkCenter")
    
    __table_args__ = (
        Index("idx_routing_ops_routing", "routing_id"),
        Index("idx_routing_ops_sequence", "routing_id", "sequence"),
    )


# ==================== ORDER MODELS ====================

class Order(Base, TimestampMixin):
    """Заказ на производство"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), nullable=False, unique=True)
    customer_id = Column(Integer, nullable=True)  # ID клиента (может быть внешняя таблица)
    priority = Column(Integer, default=5, nullable=False)  # 1-наивысший, 10-низший
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=False)
    order_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    notes = Column(Text, nullable=True)
    
    # Связи
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    operations = relationship("Operation", back_populates="order", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_orders_number", "order_number"),
        Index("idx_orders_status", "status"),
        Index("idx_orders_due_date", "due_date"),
    )


class OrderItem(Base, TimestampMixin):
    """Позиция заказа"""
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    quantity_completed = Column(Float, default=0.0, nullable=False)
    unit_price = Column(Float, nullable=True)
    
    # Связи
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
    
    __table_args__ = (
        Index("idx_order_items_order", "order_id"),
        Index("idx_order_items_product", "product_id"),
    )


class Operation(Base, TimestampMixin):
    """Производственная операция"""
    __tablename__ = "operations"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    order_item_id = Column(Integer, ForeignKey("order_items.id"), nullable=True)
    work_center_id = Column(Integer, ForeignKey("work_centers.id"), nullable=False)
    sequence = Column(Integer, nullable=False)
    status = Column(SQLEnum(OperationStatus), default=OperationStatus.NOT_STARTED, nullable=False)
    planned_start = Column(DateTime(timezone=True), nullable=True)
    planned_end = Column(DateTime(timezone=True), nullable=True)
    actual_start = Column(DateTime(timezone=True), nullable=True)
    actual_end = Column(DateTime(timezone=True), nullable=True)
    setup_time = Column(Float, default=0.0, nullable=False)
    run_time = Column(Float, default=0.0, nullable=False)
    quantity = Column(Float, nullable=False)
    quantity_good = Column(Float, default=0.0, nullable=False)
    quantity_scrap = Column(Float, default=0.0, nullable=False)
    notes = Column(Text, nullable=True)
    
    # Связи
    order = relationship("Order", back_populates="operations")
    work_center = relationship("WorkCenter", back_populates="operations")
    resources = relationship("OperationResource", back_populates="operation", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_operations_order", "order_id"),
        Index("idx_operations_work_center", "work_center_id"),
        Index("idx_operations_status", "status"),
        Index("idx_operations_planned_start", "planned_start"),
    )


class OperationResource(Base, TimestampMixin):
    """Назначение ресурсов на операцию"""
    __tablename__ = "operation_resources"
    
    id = Column(Integer, primary_key=True, index=True)
    operation_id = Column(Integer, ForeignKey("operations.id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    quantity_required = Column(Float, default=1.0, nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
    
    # Связи
    operation = relationship("Operation", back_populates="resources")
    resource = relationship("Resource", back_populates="operation_resources")
    
    __table_args__ = (
        Index("idx_op_res_operation", "operation_id"),
        Index("idx_op_res_resource", "resource_id"),
    )


# ==================== WAREHOUSE MODELS ====================

class Warehouse(Base, TimestampMixin):
    """Склад"""
    __tablename__ = "warehouses"
    
    id = Column(Integer, primary_key=True, index=True)
    enterprise_id = Column(Integer, ForeignKey("enterprises.id"), nullable=False)
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False)
    location = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Связи
    enterprise = relationship("Enterprise", back_populates="warehouses")
    inventory = relationship("Inventory", back_populates="warehouse", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_warehouses_enterprise", "enterprise_id"),
    )


class Inventory(Base, TimestampMixin):
    """Запасы материалов/продуктов"""
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity_on_hand = Column(Float, default=0.0, nullable=False)
    quantity_reserved = Column(Float, default=0.0, nullable=False)
    quantity_available = Column(Float, default=0.0, nullable=False)
    reorder_point = Column(Float, nullable=True)  # Точка перезаказа
    reorder_quantity = Column(Float, nullable=True)  # Количество для заказа
    
    # Связи
    warehouse = relationship("Warehouse", back_populates="inventory")
    product = relationship("Product")
    
    __table_args__ = (
        Index("idx_inventory_warehouse", "warehouse_id"),
        Index("idx_inventory_product", "product_id"),
        Index("idx_inventory_available", "quantity_available"),
    )


# ==================== PLANNING MODELS ====================

class ProductionPlan(Base, TimestampMixin):
    """Производственный план"""
    __tablename__ = "production_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_name = Column(String(255), nullable=False)
    plan_type = Column(String(50), nullable=False)  # daily, weekly, monthly
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(50), default="draft", nullable=False)  # draft, active, completed, archived
    created_by = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Связи
    plan_operations = relationship("PlannedOperation", back_populates="plan", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_plan_dates", "start_date", "end_date"),
        Index("idx_plan_status", "status"),
    )


class PlannedOperation(Base, TimestampMixin):
    """Запланированная операция в плане"""
    __tablename__ = "planned_operations"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("production_plans.id"), nullable=False)
    operation_id = Column(Integer, ForeignKey("operations.id"), nullable=True)
    work_center_id = Column(Integer, ForeignKey("work_centers.id"), nullable=False)
    scheduled_start = Column(DateTime(timezone=True), nullable=False)
    scheduled_end = Column(DateTime(timezone=True), nullable=False)
    resource_allocation = Column(Text, nullable=True)  # JSON с распределением ресурсов
    is_confirmed = Column(Boolean, default=False, nullable=False)
    
    # Связи
    plan = relationship("ProductionPlan", back_populates="plan_operations")
    operation = relationship("Operation")
    work_center = relationship("WorkCenter")
    
    __table_args__ = (
        Index("idx_planned_ops_plan", "plan_id"),
        Index("idx_planned_ops_schedule", "scheduled_start", "scheduled_end"),
    )

class Material(Base, TimestampMixin):
    '''Справочник материалов'''
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    article = Column(String(100), unique=True, nullable=False, index=True)
    counterparty = Column(String(255), nullable=True)
    accounting_model = Column(String(100), nullable=True)
    shelf_life = Column(Integer, nullable=True)  # Срок хранения в днях

    __table_args__ = (
        Index("idx_materials_name", "name"),
        Index("idx_materials_article", "article"),
    )
