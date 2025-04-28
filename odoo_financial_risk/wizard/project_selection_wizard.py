from odoo import models, fields, api

class ProjectSelectionWizard(models.TransientModel):
    _name = 'project.selection.wizard'
    _description = '批量选择项目向导'

    selected_projects = fields.Many2many(
        'dues.income.expenditure.items',
        string='选择项目'
    )

    def action_add_projects(self):
        """将选中的项目按行插入明细表"""
        active_id = self.env.context.get('active_id')
        main_record = self.env['dues.income.expenditure'].browse(active_id)
        for project in self.selected_projects:
            print(project)
            print(project.type)
            self.env['dues.income.expenditure.line'].create({
                'due_id': main_record.id,
                'project_ids': [(4, project.id)],
                'type': project.type,
                'subtotal': 0.0,  # 初始值设为0，用户可手动修改
                'current_level_amount': 0.0,
                'next_level_amount': 0.0,
            })
        return {'type': 'ir.actions.act_window_close'}