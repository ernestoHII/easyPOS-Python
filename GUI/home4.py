from imports import *

file_path = 'POS-type.ini'
# Usage
# pos_type_value = read_pos_type_from_ini(file_path)
# print(f"POS type is: {pos_type_value}")

def add_or_select_tab(tab_widget, widget, label):
    # Check if the tab exists
    for index in range(tab_widget.count()):
        if tab_widget.tabText(index) == label:
            # Tab exists, select it
            tab_widget.setCurrentIndex(index)
            return
    
    # If the tab does not exist, add and select
    tab_widget.addTab(widget, label)
    tab_widget.setCurrentWidget(widget)
    
class EmbeddedItemDetail(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_ItemDetail()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.ui.pushButtonClose.clicked.connect(self.close_tab)
        self.ui.pushButtonAddItemPrice.clicked.connect(self.open_ItemPriceDetail)
        self.ui.pushButtonAddItemComponent.clicked.connect(self.open_ItemComponentDetail)
        self.ui.pushButtonAddItemPackage.clicked.connect(self.open_Ui_DialogItemPackageDetail)
        self.ui.pushButtonAddItemAddOns.clicked.connect(self.open_Ui_DialogItemAddOnDetail)
        self.ui.pushButtonAddItemModifier.clicked.connect(self.open_Ui_DialogItemModifierDetail)

    def open_ItemPriceDetail(self):
        self.dialog = QDialog(self)
        self.ui_dialog = Ui_DialogItemPriceDetail()
        self.ui_dialog.setupUi(self.dialog)
        self.ui_dialog.pushButton_7.clicked.connect(self.dialog.close)
        self.dialog.show()
    
    def open_ItemComponentDetail(self):
        self.dialog = QDialog(self)
        self.ui_ItemComponentDetail = Ui_DialogItemComponentDetail()
        self.ui_ItemComponentDetail.setupUi(self.dialog)        
        self.ui_ItemComponentDetail.pushButton_7.clicked.connect(self.dialog.close)
        self.dialog.show()

    def open_Ui_DialogItemPackageDetail(self):    
        self.dialog = QDialog(self)                    
        self.ui_ItemPackageDetail = Ui_DialogItemPackageDetail()
        self.ui_ItemPackageDetail.setupUi(self.dialog)   
        self.ui_ItemPackageDetail.pushButton_7.clicked.connect(self.dialog.close)
        self.dialog.show()

    def open_Ui_DialogItemAddOnDetail(self):               
        self.dialog = QDialog(self)              
        self.ui_ItemAddOnDetail = Ui_DialogItemAddOnDetail()
        self.ui_ItemAddOnDetail.setupUi(self.dialog)  
        self.ui_ItemAddOnDetail.pushButton_7.clicked.connect(self.dialog.close)
        self.dialog.show()
        
    def open_Ui_DialogItemModifierDetail(self):        
        self.dialog = QDialog(self)        
        self.ui_ItemModifierDetail = Ui_DialogItemModifierDetail()
        self.ui_ItemModifierDetail.setupUi(self.dialog)                          
        self.ui_ItemModifierDetail.pushButton_7.clicked.connect(self.dialog.close)        
        self.dialog.show()
        
    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here

class EmbeddedItemList(QWidget):
    def __init__(self, main_window, tab_widget, menu_instance):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_FormList()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.ui.pushButtonClose.clicked.connect(self.close_tab)
        self.ui.pushButtonAdd.clicked.connect(self.open_item_detail)
        
        # Connect the textChanged signal of the search input to the search_data function
        # self.ui.textEditItemFilter.textChanged.connect(self.search_data)        
        # Call the load_table_headers method on the menu_instance
        menu_instance.load_table_headers(self.ui.tableWidget)      
        # menu_instance.update_data(self.ui.tableWidget)  # <-- This line calls the method from Menu class
        # Populate the comboBoxIsInventoryFilter with options
        self.ui.comboBoxIsInventoryFilter.addItems(["All", "Inventory", "Non-Inventory"])
        # Connect the currentIndexChanged signal to update the data                        
        # Populate the comboBoxIsLockedFilter with options
        self.ui.comboBoxIsLockedFilter.addItems(["All", "Locked", "Unlocked"])
        # Connect the currentIndexChanged signal to update the data
                  
    def close_tab(self):
        # index = self.main_window.tab_widget.indexOf(self)
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here

    def open_item_detail(self):  # New method
        tab_item = EmbeddedItemDetail(self.main_window, self.tab_widget)
        add_or_select_tab(self.main_window.tab_widget, tab_item, "Setup - Item Detail")

class EmbeddedPOSTouchQuickServiceList(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_POSTouchQuickService()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.ui.pushButtonClose.clicked.connect(self.close_tab)
        self.ui.pushButtonWalkIn.clicked.connect(self.open_POSTouchQuickServiceDetail)
        self.ui.pushButtonDelivery.clicked.connect(self.open_delivery)

    def open_delivery(self):
        self.popup = EmbeddedPOSDeliveryCustomerInformation(self.main_window, self.tab_widget)  # Pass both required arguments
        self.popup.show()    
    def open_POSTouchQuickServiceDetail(self):
        pos_tab = EmbeddedPOSTouchQuickServiceDetail(self.main_window, self.tab_widget)
        add_or_select_tab(self.main_window.tab_widget, pos_tab, "Quick Service Detail")
    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here
class EmbeddedPOSDeliveryCustomerInformation(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = UI_POSDeliveryCustomerInformation()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget    
        self.ui.pushButtonClose.clicked.connect(self.close)     
        self.ui.pushButtonOk.clicked.connect(self.open_POSTouchQuickServiceDetail) 
    def open_POSTouchQuickServiceDetail(self):
        pos_tab = EmbeddedPOSTouchQuickServiceDetail(self.main_window, self.tab_widget)
        add_or_select_tab(self.main_window.tab_widget, pos_tab, "Quick Service Detail")
        self.close()
        
class EmbeddedPOSTouchQuickServiceDetail(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_POSTouchQuickServiceDetail()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.ui.pushButtonClose.clicked.connect(self.close_tab)
        self.ui.pushButtonTender.clicked.connect(self.open_Tender)  # Changed this line
        self.ui.pushButtonSearchItem.clicked.connect(self.open_discount_search_item_detail)
        self.ui.pushButtonOverride.clicked.connect(self.open_override)
        self.ui.pushButtonDiscount.clicked.connect(self.open_discount)
        self.ui.pushButtonReturn.clicked.connect(self.open_return)
        self.ui.pushButtonLock.clicked.connect(self.open_lock)
        self.ui.pushButtonCurrency.clicked.connect(self.open_currencyk)
        self.ui.pushButtonItem1.clicked.connect(self.open_sales_item)

    def open_sales_item(self):  # New method to open the dialog
        self.popup = EmbeddedPOSSalesItemDetail(self.main_window, self.tab_widget)  # Pass both required arguments
        self.popup.show()     
    def open_currencyk(self):  # New method to open the dialog
        self.popup = EmbeddedPOSSearchCurrency(self.main_window, self.tab_widget)  # Pass both required arguments
        self.popup.show()       
    def open_lock(self):  # New method to open the dialog
        self.popup = EmbeddedPOSSalesCustomerDetail(self.main_window, self.tab_widget)  # Pass both required arguments
        self.popup.show()   
    def open_return(self):  # New method to open the dialog
        self.popup = EmbeddedReturn(self.main_window, self.tab_widget)  # Pass both required arguments
        self.popup.show()          
    def open_discount(self):  # New method to open the dialog
        self.popup = EmbeddedDiscount(self.main_window, self.tab_widget)  # Pass both required arguments
        self.popup.show()           
    def open_override(self):  # New method to open the dialog
        self.popup = EmbeddedLogin(self.main_window, self.tab_widget)  # Pass both required arguments
        self.popup.show()                
    def open_discount_search_item_detail(self):  # New method to open the dialog
        self.popup = EmbeddedDiscountSearchItemDetail(self.main_window, self.tab_widget)  # Pass both required arguments
        self.popup.show()
    def open_Tender(self):  # New method to open the dialog
        self.popup = EmbeddedPOSBarcodeTender(self.main_window, self.tab_widget)  # Pass both required arguments
        self.popup.show()                
    def open_tab(self):
        openTab = Ui_POSTouchQuickServiceDetail(self.main_window, self.tab_widget)
        add_or_select_tab(self.main_window.tab_widget, openTab, "Quick Service Detail")
    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here 

class EmbeddedPOSSalesItemDetail(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = UI_POSSalesItemDetail()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget    
        self.ui.pushButtonClose.clicked.connect(self.close)  
class EmbeddedPOSSalesCustomerDetail(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = UI_POSSalesCustomerDetail()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget    
        self.ui.pushButtonClose.clicked.connect(self.close)  

class EmbeddedPOSSearchCurrency(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = UI_POSSearchCurrency()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget    
        self.ui.pushButtonClose.clicked.connect(self.close)  
class EmbeddedReturn(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = UI_POSReturnRefund()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget    
        self.ui.pushButtonClose.clicked.connect(self.close)  
class EmbeddedDiscount(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = UI_POSDiscount()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget    
        self.ui.pushButtonClose.clicked.connect(self.close)         
class EmbeddedLogin(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = UI_Login()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget    
        self.ui.pushButtonClose.clicked.connect(self.close)                                                                     
class EmbeddedPOSTouchSalesList(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_POSTouchSalesList()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.ui.pushButtonClose.clicked.connect(self.close_tab)
        self.ui.pushButtonWalkIn.clicked.connect(self.open_POSTouchSalesDetail)

    def open_POSTouchSalesDetail(self):
        openTab = EmbeddedPOSTouchSalesDetail(self.main_window, self.tab_widget)
        add_or_select_tab(self.main_window.tab_widget, openTab, "Activity - POS Touch Detail")
        
    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here

class EmbeddedPOSTouchSalesDetail(QWidget): #dodo
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_POSTouchSalesDetail()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.ui.pushButtonClose.clicked.connect(self.close_tab)
        self.ui.pushButtonTender.clicked.connect(self.open_Tender)

    def open_Tender(self):  # New method to open the dialog
        self.popup = EmbeddedPOSBarcodeTender(self.main_window, self.tab_widget)  # Pass both required arguments
        self.popup.show()           
    def open_tab(self):
        openTab = Ui_POSTouchQuickServiceDetail(self.main_window, self.tab_widget)
        add_or_select_tab(self.main_window.tab_widget, openTab, "Quick Service Detail")        
    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here

class EmbeddedPOSBarcode(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_POSBarcode()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.ui.pushButtonClose.clicked.connect(self.close_tab)
        self.ui.pushButton_11.clicked.connect(self.open_POSBarcodeDetail)
        self.ui.pushButton_10.clicked.connect(self.open_Tender)  # Changed this line
    
    def open_Tender(self):  # New method to open the dialog
        self.popup = EmbeddedPOSBarcodeTender(self.main_window, self.tab_widget)  # Pass both required arguments
        self.popup.show()   
    def open_POSBarcodeDetail(self):
        openTab = EmbeddedPOSBarcodeDetail(self.main_window, self.tab_widget)
        add_or_select_tab(self.main_window.tab_widget, openTab, "Activity - POS Barcode Detail")
                        
    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here

class EmbeddedPOSBarcodeDetail(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_POSBarcodeDetail()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.ui.pushButtonClose.clicked.connect(self.close_tab)
        self.ui.pushButton_3.clicked.connect(self.open_Tender)
        self.ui.pushButton_35.clicked.connect(self.open_discount_search_item_detail)

    def open_discount_search_item_detail(self):  # New method to open the dialog
        self.popup = EmbeddedDiscountSearchItemDetail(self.main_window, self.tab_widget)  # Pass both required arguments
        self.popup.show()
    def open_Tender(self):  # New method to open the dialog
        self.popup = EmbeddedPOSBarcodeTender(self.main_window, self.tab_widget)  # Pass both required arguments
        self.popup.show()    
    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here

class EmbeddedPOSBarcodeTender(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.tab_widget = tab_widget
        self.ui = Ui_POSBarcodeTender()
        self.ui.setupUi(self)                
        self.ui.pushButtonClose.clicked.connect(self.close_tab)
        # self.ui.pushButton_3.clicked.connect(self.open_pos_barcode_detail)
        self.ui.pushButtonClose.clicked.connect(self.close)  # 'self.close' is a method provided by QWidget to close the widget
        
    # def open_pos_barcode_detail(self):
    #     openTab = EmbeddedPOSBarcodeDetail(self.main_window, self.tab_widget)
    #     add_or_select_tab(self.main_window.tab_widget, openTab, "Activity - POS Barcode Detail")
                
    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here                

class EmbeddedCustomerListCombinedApp(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_CustomerList()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.ui.pushButtonClose.clicked.connect(self.close_tab)
        self.ui.pushButtonAdd.clicked.connect(self.open_CustomerDetailCombinedApp)

    def open_CustomerDetailCombinedApp(self):
        openTab = EmbeddedCustomerDetailCombinedApp(self.main_window, self.tab_widget)
        add_or_select_tab(self.main_window.tab_widget, openTab, "Setup - Customer List")
        
    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here

class EmbeddedCustomerDetailCombinedApp(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_CustomerDetail()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.ui.pushButtonClose.clicked.connect(self.close_tab)

    def open_tab(self):
        openTab = Ui_POSTouchQuickServiceDetail(self.main_window, self.tab_widget)
        add_or_select_tab(self.main_window.tab_widget, openTab, "Setup - Customer Detail")
        
    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here

class EmbeddedDiscountList(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_DiscountList()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.ui.pushButtonClose.clicked.connect(self.close_tab)
        self.ui.pushButtonAdd.clicked.connect(self.open_CustomerDetailCombinedApp)

    def open_CustomerDetailCombinedApp(self):
        openTab = EmbeddedDiscountDetail(self.main_window, self.tab_widget)
        add_or_select_tab(self.main_window.tab_widget, openTab, "Setup - Discounting Detail")
        
    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here

class EmbeddedDiscountDetail(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_DiscountDetail()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.ui.pushButtonClose.clicked.connect(self.close_tab)
        self.ui.btnSearch.clicked.connect(self.open_discount_search_item_detail)

    def open_discount_search_item_detail(self):  # New method to open the dialog
        self.popup = EmbeddedDiscountSearchItemDetail(self.main_window, self.tab_widget)  # Pass both required arguments
        self.popup.show()
        
    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here    

class EmbeddedDiscountSearchItemDetail(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_DiscountSearchItemDetail()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.ui.pushButtonClose.clicked.connect(self.close_tab)
        self.ui.pushButtonClose.clicked.connect(self.close)  # 'self.close' is a method provided by QWidget to close the widget
        
    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here  
                    
class EmbeddedUserList(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_UserList()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.ui.btnClose.clicked.connect(self.close_tab)
        self.ui.btnAdd.clicked.connect(self.open_POSTouchQuickServiceDetail)

    def open_POSTouchQuickServiceDetail(self):
        pos_tab = EmbeddedUserDetail(self.main_window, self.tab_widget)
        add_or_select_tab(self.main_window.tab_widget, pos_tab, "Setup - User Detail")
        
    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here

class EmbeddedUserDetail(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_UserDetail()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.ui.btnClose.clicked.connect(self.close_tab)
        # self.ui.pushButtonTender.clicked.connect(self.open_pop1)  # Changed this line
        # self.ui.pushButtonSearchItem.clicked.connect(self.open_pop2)

    def open_pop1(self):  # New method to open the dialog
        # self.popup = EmbeddedDiscountSearchItemDetail(self.main_window, self.tab_widget)  # Pass both required arguments
        # self.popup.show()
        pass
    def open_pop2(self):  # New method to open the dialog
        # self.popup = EmbeddedPOSBarcodeTender(self.main_window, self.tab_widget)  # Pass both required arguments
        # self.popup.show()  
        pass              
    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here

class EmbeddedSYSTables(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_SYSTables()
        self.ui.setupUi(self)
        self.tab_widget = self.ui.tabWidget        
        self.ui.pushButtonClose.clicked.connect(self.close_tab)
        self.ui.pushButtonAdd.clicked.connect(self.open_pop1)

    def open_pop1(self): 
        # Determine the action based on the title of the currently selected tab
        current_tab_text = self.tab_widget.tabText(self.tab_widget.currentIndex())
        if current_tab_text == "Account":
            self.popup = EmbeddedAccountDetail(self.main_window, self.tab_widget)
            self.popup.show()  # Make sure to show the popup.            
        elif current_tab_text == "Pay Type":
            self.popup = EmbeddedPayTypeDetail(self.main_window, self.tab_widget)
            self.popup.show()  # Make sure to show the popup.
        elif current_tab_text == "Bank":
            self.popup = EmbeddedBankDetail(self.main_window, self.tab_widget)
            self.popup.show()  # Make sure to show the popup.
        elif current_tab_text == "Unit":
            self.popup = EmbeddedUnitDetail(self.main_window, self.tab_widget)
            self.popup.show()  # Make sure to show the popup.
        elif current_tab_text == "Terminal":
            self.popup = EmbeddedTerminalDetail(self.main_window, self.tab_widget)
            self.popup.show()  # Make sure to show the popup.
        elif current_tab_text == "Tax":
            self.popup = EmbeddedTaxDetail(self.main_window, self.tab_widget)
            self.popup.show()  # Make sure to show the popup.
        elif current_tab_text == "Supplier":
            self.popup = EmbeddedSupplierDetail(self.main_window, self.tab_widget)
            self.popup.show()  # Make sure to show the popup.
        elif current_tab_text == "Period":
            self.popup = EmbeddedPeriodDetail(self.main_window, self.tab_widget)
            self.popup.show()  # Make sure to show the popup.
        elif current_tab_text == "Form":
            self.popup = EmbeddedFormDetail(self.main_window, self.tab_widget)
            self.popup.show()  # Make sure to show the popup.
        elif current_tab_text == "Item Category":
            self.popup = EmbeddedItemCategoryDetail(self.main_window, self.tab_widget)
            self.popup.show()  # Make sure to show the popup.
        elif current_tab_text == "Card Type":
            self.popup = EmbeddedCardTypeDetail(self.main_window, self.tab_widget)
            self.popup.show()  # Make sure to show the popup.

    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here
        
class EmbeddedBankDetail(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = UI_BankDetail()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget    
        self.ui.btnClose.clicked.connect(self.close)    

class EmbeddedCardTypeDetail(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = UI_CardTypeDetail()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget    
        self.ui.btnClose.clicked.connect(self.close)  
class EmbeddedFormDetail(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = UI_FormDetail()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget    
        self.ui.btnClose.clicked.connect(self.close)      

class EmbeddedPeriodDetail(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = UI_PeriodDetail()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget    
        self.ui.btnClose.clicked.connect(self.close)      
class EmbeddedSupplierDetail(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = UI_SupplierDetail()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget    
        self.ui.btnClose.clicked.connect(self.close)      
class EmbeddedTaxDetail(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = UI_TaxDetail()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget    
        self.ui.btnClose.clicked.connect(self.close)      
class EmbeddedTerminalDetail(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = UI_TerminalDetail()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget    
        self.ui.btnClose.clicked.connect(self.close)      
class EmbeddedAccountDetail(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = UI_AccountDetail()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget    
        self.ui.pushButtonClose.clicked.connect(self.close)      
class EmbeddedUnitDetail(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = UI_UnitDetail()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget    
        self.ui.btnClose.clicked.connect(self.close)     
         
class EmbeddedItemCategoryDetail(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = UI_ItemCategoryDetail()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget    
        self.ui.btnClose.clicked.connect(self.close)       

class EmbeddedPayTypeDetail(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = UI_PayTypeDetail()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget    
        self.ui.pushButtonClose.clicked.connect(self.close)    
                        
class Menu(QMainWindow):
    def __init__(self, tab_widget):
        super().__init__()
        self.tab_widget = tab_widget  # Store the tab widget
        self.total_count = 0  # Initialize total_count        
        self.setWindowTitle("POS - GPT")

        # Get the screen resolution
        screen_resolution = QDesktopWidget().screenGeometry(0)  # For the primary screen
        # Adjust geometry based on resolution
        if screen_resolution.width() == 1280 and screen_resolution.height() == 1024:
            self.setGeometry(0, 0, 1280, 956)
        elif screen_resolution.width() == 1366 and screen_resolution.height() == 768:
            self.setGeometry(0, 0, 1366, 500)
        else:
            # Default size, can be adjusted
            self.setGeometry(0, 0, 1366, 500)   
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        # Create a layout for the central widget
        central_layout = QVBoxLayout(central_widget)
        grid_layout = QGridLayout()  # We create this layout here, but it isn't attached yet.
        # Initialize variables to keep track of the current page and number of items per page
        self.current_page = 1
        self.items_per_page = 20

        # Create and add buttons to the grid layout
        button_info = [
            ("Item", "img/Item.png"), ("POS - F2", "img/POS.png"), ("Sales Report", "img/Reports.png"), ("POS Report", "img/Reports.png"),
            ("Discounting", "img/Discounting.png"), ("Cash In/Out", "img/Disbursement.png"), ("Remittance Report", "img/Reports.png"),
            ("Settings", "img/Settings.png"), ("Customer", "img/Customer.png"), ("Stock In", "img/Stock In.png"),
            ("Inventory Report", "img/Reports.png"), ("Utilities", "img/Utilities.png"), ("User", "img/User.png"), ("Stock Out", "img/Stock Out.png"),
            ("Stock Count", "img/Stock Count.png"), ("System Tables", "img/System Tables.png")]

        # Create a list of values for the buttons
        button_values = [
            "Setup - Item List", "POS - F2", "Sales Report", "POS Report", "Discounting", "Cash In/Out", "Remittance Report", "Settings", "Customer", "Stock In",
            "Inventory Report", "Utilities", "User", "Stock Out", "Stock Count", "System Tables"]

        for row in range(4):
            for col in range(4):
                index = row * 4 + col
                if index < len(button_info):
                    button_text, icon_path = button_info[index]
                    button_value = button_values[index]  # Get the value for this button
                    container = QWidget()
                    layout = QVBoxLayout(container)
                    button = QPushButton()
                    size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                    button.setSizePolicy(size_policy)
                    pixmap = QPixmap()
                    if not pixmap.load(icon_path):
                        print("Error loading image:", pixmap.isNull())
                    else:
                        pixmap = pixmap.scaledToHeight(90)  # Adjusted to be 5% smaller
                        icon = QIcon(pixmap)
                        button.setIcon(icon)
                        button.setIconSize(pixmap.size())
                    # Create a label for the button title (text)
                    title_label = QLabel(button_text)
                    title_label.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)  # Align text to the bottom center
                    # Make the text bold
                    font = QFont()
                    font.setBold(True)
                    title_label.setFont(font)
                    layout.addWidget(button)
                    layout.addWidget(title_label)
                    grid_layout.addWidget(container, row, col)
                    # Connect a function to the button's clicked signal
                    button.clicked.connect(lambda _, value=button_value: self.create_tab(value))
        self.rows = []  # Initialize rows as an empty list
        # Add the grid layout to the central layout
        central_layout.addLayout(grid_layout)

    def create_tab(self, button_value):
        
        if self.tab_widget is not None:
            for index in range(self.tab_widget.count()):
                if self.tab_widget.tabText(index) == button_value:
                    self.tab_widget.setCurrentIndex(index)
                    return
            if button_value == "Setup - Item List":
                listTab = EmbeddedItemList(self, self.tab_widget, self)                    
                add_or_select_tab(self.tab_widget, listTab, "Setup - Item List")
            elif button_value == "POS - F2":
                pos_type_value = read_pos_type_from_ini(file_path)
                print(pos_type_value)
                if pos_type_value == 3:
                    posTab = EmbeddedPOSTouchQuickServiceList(self, self.tab_widget)
                    add_or_select_tab(self.tab_widget, posTab, "Activity - POS Touch Quick Service")
                elif pos_type_value == 2:
                    PTSLTab = EmbeddedPOSTouchSalesList(self, self.tab_widget)
                    add_or_select_tab(self.tab_widget, PTSLTab, "Activity - POS Touch")           
                elif pos_type_value == 1:
                    barcodeTab = EmbeddedPOSBarcode(self, self.tab_widget)
                    add_or_select_tab(self.tab_widget, barcodeTab, "Activity - POS Barcode")                        
            elif button_value == "Customer":
                customerTab = EmbeddedCustomerListCombinedApp(self, self.tab_widget)
                add_or_select_tab(self.tab_widget, customerTab, "Setup - Customer")                                
            elif button_value == "Discounting":
                discountTab = EmbeddedDiscountList(self, self.tab_widget)
                add_or_select_tab(self.tab_widget, discountTab, "Setup - Discounting List")                                    
            elif button_value == "User":
                userTab = EmbeddedUserList(self, self.tab_widget)
                add_or_select_tab(self.tab_widget, userTab, "Setup - User List")    
            elif button_value == "System Tables":
                sub_tab_widget = QTabWidget()  # This is just an example. You should create or reference the actual sub-tab widget here.
                systemTablesInstance = EmbeddedSYSTables(self, sub_tab_widget)
                # Add the EmbeddedSYSTables instance as a tab within sub_tab_widget.
                # You can specify the tab title as "System - System Tables" or customize it as needed.
                sub_tab_widget.addTab(systemTablesInstance, "System - System Tables")
                
                add_or_select_tab(self.tab_widget, systemTablesInstance, "System - System Tables")
                
    def load_next_page(self, table_widget):
        # Check if there are more pages to load
        total_pages = max(1, -(-self.total_count // self.items_per_page))
        if self.current_page < total_pages:
            self.current_page += 1
            self.load_table_headers(table_widget)

    def load_prev_page(self, table_widget):
        if self.current_page > 1:  # Avoid going into negative or zero pages
            self.current_page -= 1  # decrement the current page here
            self.load_table_headers(table_widget)
                                                                                                                              
    def load_first_page(self, table_widget):
        self.current_page = 1
        self.load_table_headers(table_widget)

    def load_last_page(self, table_widget):
        self.current_page = -(-self.total_count // self.items_per_page)  # Calculate total pages dynamically
        self.load_table_headers(table_widget)

    def close_current_tab(self):
        print("Loaded4")            
        # Get the index of the current tab
        current_index = self.tab_widget.currentIndex()
        
        # Remove the current tab
        self.tab_widget.removeTab(current_index)

    def show_error_message(self, msg):
        QMessageBox.critical(self, "Error", msg)

    def load_table_headers(self, table_widget):
        # Define the endpoint URL
        url = "http://127.0.0.1:8000/items/"

        response = requests.get(url)

        # Ensure the request was successful
        if response.status_code == 200:
            data = response.json()
            print(data)  # Print the fetched data
            items_list = data.get("items", [])

            if items_list:
                headers = list(items_list[0].keys())
                table_widget.setHorizontalHeaderLabels(headers)

                # Set the number of rows and columns
                table_widget.setRowCount(len(items_list))
                table_widget.setColumnCount(len(headers))
                
                # Populate the table with data
                for row_num, item in enumerate(items_list):
                    for col_num, key in enumerate(headers):
                        cell_value = item[key]
                        table_widget.setItem(row_num, col_num, QTableWidgetItem(str(cell_value)))

                # Set each column width to fit the longest values from each row
                for col_num in range(len(headers)):
                    max_width = max(table_widget.columnWidth(col_num), table_widget.sizeHintForColumn(col_num))
                    table_widget.setColumnWidth(col_num, max_width)
                    
            else:
                # No items found
                table_widget.setRowCount(0)
                table_widget.setColumnCount(0)
                
        else:
            # Handle errors, perhaps log them or show an error message
            print(f"Error fetching items: {response.status_code} - {response.text}")

        gc.collect()  # <-- Added for cleaning up after loading and processing data


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Tabbed Grid of Buttons")
        self.setGeometry(0, 0, 1366, 690)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        # Create a tab widget
        self.tab_widget = QTabWidget()
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(self.tab_widget)
        # Add "Menu" tab and pass the tab_widget to the Menu class
        menu_tab = Menu(self.tab_widget)
        self.tab_widget.addTab(menu_tab, "Menu")

def read_pos_type_from_ini(file_path):
    config = configparser.ConfigParser()

    # Check if the file exists
    if not os.path.exists(file_path):
        # If it doesn't exist, create it with default values
        config['POStype'] = {'type': '3'}
        with open(file_path, 'w') as configfile:
            config.write(configfile)

    config.read(file_path)

    try:
        pos_type = config.get('POStype', 'type')
        return int(pos_type)
    except configparser.NoSectionError:
        print(f"Error: No section 'POStype' found in {file_path}")
    except configparser.NoOptionError:
        print(f"Error: No option 'type' found in section 'POStype' of {file_path}")
    except ValueError:
        print(f"Error: Invalid value for 'type' in {file_path}. It should be an integer.")
    except Exception as e:
        print(f"Unexpected error reading {file_path}: {e}")

    return None

class BackendCommunication:
    BASE_URL = "http://localhost:8000"  # Replace with your backend URL

    @staticmethod
    def load_data(page, custom_offset, is_locked_filter, is_inventory_filter):
        url = f"{BackendCommunication.BASE_URL}/load_data"
        params = {
            "page": page,
            "custom_offset": custom_offset,
            "is_locked_filter": is_locked_filter,
            "is_inventory_filter": is_inventory_filter
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())


