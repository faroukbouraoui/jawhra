def _compute_poid_brut_(self):
    if self.order_id.is_export == False:
        self.poid_brut = self.product_uom_qty * 1.06
    elif self.order_id.is_export == True:
        self.product_uom_qty = self.qte_nette - self.qte_caisse * self.poid_caisse