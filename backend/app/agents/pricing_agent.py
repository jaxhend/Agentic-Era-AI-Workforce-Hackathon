from backend.app.schemas.schemas import PricingIn, PricingOut

def quote(data: PricingIn) -> PricingOut:
    breakdown = []
    subtotal = 0.0
    for it in data.items:
        line_total = it.qty * it.unit_price
        subtotal += line_total
        breakdown.append({"name": it.name, "qty": it.qty, "unit_price": it.unit_price, "line_total": round(line_total, 2)})
    discount = round(subtotal * (data.discount_pct / 100.0), 2)
    vat_base = subtotal - discount
    vat = round(vat_base * (data.vat_pct / 100.0), 2)
    total = round(vat_base + vat, 2)
    return PricingOut(subtotal=round(subtotal, 2), discount=discount, vat=vat, total=total, breakdown=breakdown)

