# AgriLink integrated workspaces

AgriLink exposes six workspaces: Farmer Intelligence, Mandi Price Intelligence, Store Demand Intelligence, Inventory Intelligence, the Integrated Intelligence page, and the AgriLink Overall Decision Dashboard. The Integrated Intelligence page has two sections: Integration 01 (Farmer + Mandi) at the top, and Integration 02 (Store Demand + Inventory) below it.

The Store Demand + Inventory section runs the existing demand regressor and inventory risk classifier independently, then combines their outputs with transparent stock-gap logic. The current retail demand data uses Store ID and Product ID; the inventory data uses SKU-level records and does not contain a verified common product/SKU key. Therefore, the page asks for inventory-model signals separately and does not fabricate a join. The stock-gap calculation is `max(0, forecast demand - (current stock + units already ordered))`. This is a basic planning estimate, not an optimized replenishment quantity; it does not include safety stock or supplier lead-time policy.

The Overall Decision Dashboard summarizes the four existing models and links to all six analysis workspaces. Integrated pages reuse the existing models; no additional Random Forest model is claimed or trained by the integration layer.
