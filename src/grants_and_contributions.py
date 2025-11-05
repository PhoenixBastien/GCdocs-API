from gcdocs import GCdocs


def grants_and_contributions(gcdocs: GCdocs, workspace_id: int) -> None:
    # dict of french translations of node names
    translation_dict = {
        "Payments/Monitoring": {
            "en": "Payments/Monitoring",
            "en_CA": "Payments/Monitoring",
            "fr_CA": "Paiements/surveillance",
        },
        "Payment Packages": {
            "en": "Payment Packages",
            "en_CA": "Payment Packages",
            "fr_CA": "Paquets de paiement",
        },
        "Close-out": {"en": "Close-out", "en_CA": "Close-out", "fr_CA": "Clôture"},
    }

    # create payments/monitoring and payment packages folders
    payment_packages_id = gcdocs.create_folders(
        relative_path="Payments/Monitoring:Payment Packages",
        workspace_id=workspace_id,
        translation_dict=translation_dict,
    )

    # edit payment packages folder permissions
    payment_packages_permissions = [
        {
            "name": "CMB-CIOD-IMDD - Records Office | SGM-DGDPR-DGID - Bureau des archives",
            "permissions": GCdocs.PERMISSION_TYPES,
            "type": "group",
            "action": "update",
        },
        {
            "name": "Financial Operations Group | Groupe des Opérations financières",
            "permissions": GCdocs.PERMISSION_TYPES[:2],
            "type": "group",
            "action": "update",
        },
        {
            "name": "PS-ALL",
            "workspace_id": workspace_id,
            "type": "role",
            "action": "remove",
        },
        {
            "name": "Record.Office",
            "workspace_id": workspace_id,
            "type": "role",
            "action": "remove",
        },
        {"name": "PS-All | SP-Tout", "type": "group", "action": "remove"},
    ]

    gcdocs.bulk_edit_custom_permissions(
        node_id=payment_packages_id,
        permissions=payment_packages_permissions,
        apply_to=2,
    )

    # create close-out folder
    close_out_id = gcdocs.create_folders(
        relative_path="Close-out",
        workspace_id=workspace_id,
        translation_dict=translation_dict,
    )

    # edit close-out folder permissions
    close_out_permissions = [
        {
            "name": "PS-ALL",
            "workspace_id": workspace_id,
            "permissions": GCdocs.PERMISSION_TYPES,
            "type": "role",
            "action": "update",
        }
    ]

    gcdocs.bulk_edit_custom_permissions(
        node_id=close_out_id, permissions=close_out_permissions, apply_to=2
    )

    # delete duplicate close-out folder
    gcdocs.delete_node_by_name(parent_id=workspace_id, name="Close-Out")
