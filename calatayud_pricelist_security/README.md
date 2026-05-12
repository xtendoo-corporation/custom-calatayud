# Calatayud Pricelist Security

Addon para Odoo 16 que introduce un boolean en `product.pricelist` para decidir qué tarifas pueden ver y seleccionar los usuarios sin permisos avanzados.

## Qué hace

- Crea el grupo visible **Acceso avanzado a listas de precios**.
- Añade el campo `visible_to_basic_users` en las tarifas.
- Los usuarios sin grupo avanzado solo pueden ver y seleccionar tarifas con ese boolean marcado.
- Los usuarios del grupo avanzado y administración pueden ver, crear, editar y eliminar todas las tarifas y sus reglas.
- Mantiene oculto para usuarios no avanzados el botón de gestión de reglas de tarifa en producto.

## Uso

1. Actualiza la lista de aplicaciones.
2. Instala o actualiza `calatayud_pricelist_security`.
3. Marca `Visible para usuarios básicos` en las tarifas que deban aparecer a usuarios sin permisos avanzados.
4. Añade al grupo **Acceso avanzado a listas de precios** solo a los usuarios que deban gestionar todas las tarifas.

