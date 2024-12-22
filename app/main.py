from fastapi import FastAPI, HTTPException, Depends
from typing import List
from . import models
from .database import get_db
from supabase import Client

app = FastAPI(
    title="Beauty Salon Management System",
    description="API for managing beauty salon customers",
    version="1.0.0"
)

@app.post("/customers/", response_model=models.Customer, tags=["customers"])
async def create_customer(
    customer: models.CustomerCreate,
    db: Client = Depends(get_db)
):
    """Create a new customer"""
    result = db.table("customers").insert(customer.model_dump()).execute()
    return result.data[0]

@app.get("/customers/", response_model=List[models.Customer], tags=["customers"])
async def list_customers(
    db: Client = Depends(get_db)
):
    """List all customers"""
    result = db.table("customers").select("*").execute()
    return result.data

@app.get("/customers/{customer_id}", response_model=models.Customer, tags=["customers"])
async def get_customer(
    customer_id: str,
    db: Client = Depends(get_db)
):
    """Get a specific customer by ID"""
    result = db.table("customers").select("*").eq("id", customer_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Customer not found")
    return result.data[0]

@app.patch("/customers/{customer_id}", response_model=models.Customer, tags=["customers"])
async def update_customer(
    customer_id: str,
    customer: models.CustomerUpdate,
    db: Client = Depends(get_db)
):
    """Update a customer's information"""
    update_data = {k: v for k, v in customer.model_dump().items() if v is not None}
    update_data["updated_at"] = "now()"
    
    result = db.table("customers").update(update_data).eq("id", customer_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Customer not found")
    return result.data[0]

@app.delete("/customers/{customer_id}", response_model=models.Customer, tags=["customers"])
async def deactivate_customer(
    customer_id: str,
    db: Client = Depends(get_db)
):
    """Deactivate a customer (soft delete)"""
    result = db.table("customers").update({
        "is_active": False,
        "updated_at": "now()"
    }).eq("id", customer_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Customer not found")
    return result.data[0]

@app.get("/statistics/", tags=["statistics"])
async def get_statistics(
    db: Client = Depends(get_db)
):
    """Get customer statistics"""
    active = db.table("customers").select("*", count="exact").eq("is_active", True).execute()
    inactive = db.table("customers").select("*", count="exact").eq("is_active", False).execute()
    
    return {
        "active_customers": len(active.data),
        "former_customers": len(inactive.data),
        "total_customers": len(active.data) + len(inactive.data)
    }