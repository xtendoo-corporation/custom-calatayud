# Calatayud Pricelist Security

Addon para Odoo 16 que crea el grupo `Acceso a listas de precios` y restringe la visualización y gestión de tarifas (`product.pricelist`) y reglas de tarifa (`product.pricelist.item`) únicamente a los usuarios incluidos en ese grupo.

## Qué hace

- Crea un grupo visible en **Ventas** para asignarlo desde usuarios.
- Oculta menús, botones y campos relacionados con tarifas a usuarios no autorizados.
- Reasigna los accesos del modelo para que solo ese grupo pueda leer/crear/modificar/eliminar listas de precios y sus reglas.

## Uso

1. Actualiza la lista de aplicaciones.
2. Instala el módulo `calatayud_pricelist_security`.
3. Añade los usuarios deseados al grupo **Acceso a listas de precios**.

